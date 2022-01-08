from functools import cached_property

from markdown import markdown

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now


class TodoistManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(TodoistManager, self).get_queryset().filter(todoist_id__isnull=False)


class Category(models.Model):
    """The categories of the projects."""
    name = models.CharField(max_length=20, unique=True)
    emoji = models.CharField(max_length=10)
    # TODO: Make this a unique together when it will relate to the user
    todoist_id = models.BigIntegerField(blank=True, null=True, unique=True)
    objects = models.Manager()
    todoist = TodoistManager()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.emoji + " " + self.name

    @cached_property
    def tasks_count(self) -> int:
        """Total number of tasks associated with the category."""
        return self.task_set.count()


class ActiveProjectManager(models.Manager):
    """Manager that gets only active projects by default"""
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Project(models.Model):
    """The tasks project model."""
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=8)
    # TODO: Make this a unique together when it will relate to the user
    todoist_id = models.BigIntegerField(blank=True, null=True, unique=True)
    objects = models.Manager()
    todoist = TodoistManager()
    is_active = models.BooleanField(default=True)
    active = ActiveProjectManager()

    def __str__(self) -> str:
        return "#" + self.name

    def remove_hex_prefix(self):
        """Removes the # on colors"""
        self.color = self.color.replace("#", "")

    @cached_property
    def tasks_count(self) -> int:
        """Total number of tasks associated with the project."""
        return self.task_set.count()

    @cached_property
    def repos_count(self) -> int:
        """Total number of repos associated with the project."""
        return self.repos.count()


class Task(models.Model):
    """Model to log tasks within the day"""
    created_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    task = models.CharField(max_length=400)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True,
                                blank=True)
    objects = models.Manager()
    # TODO: Make this a unique together when it will relate to the user
    todoist_id = models.BigIntegerField(blank=True, null=True)
    todoist = TodoistManager()

    class Meta:
        ordering = ['category', 'created_at']

    def __str__(self) -> str:
        return self.category.emoji + self.task

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = now()
        super(Task, self).save(*args, **kwargs)

    @property
    def rich_text(self) -> str:
        return markdown(self.task)

    def has_addon_in_task(self):
        """Checks whether the task has an addon inserted"""
        return ":" in self.task

    def extract_addons(self):
        for word in self.task.split(" "):
            if ":" in word:
                try:
                    sh = word.split(":")
                    prov = TaskAddonProvider.objects.get(shortcut=sh[0])
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    pass
                else:
                    self.create_addon(prov, word)
                finally:
                    self.task = self.task.replace(word, "")

        self.save()

    def create_addon(self, prov, word):
        sh = word.split(":")
        if sh[1] in ["", " ", None]:
            return None
        if sh[1].startswith('http'):
            TaskAddon.objects.create(
                task=self, provider=prov, url=word.split(sh[0] + ":")[1],
            )
        else:
            TaskAddon.objects.create(
                task=self, provider=prov, uid=word.split(sh[0] + ":")[1],
            )
        return None

    @property
    def pendulum_dt(self):
        """Returns the datetime in a pendulum class"""
        from pendulum.parser import parse
        return parse(str(self.created_at)).in_timezone(settings.TIME_ZONE)

    @property
    def date(self) -> str:
        """Returns the date the task was created"""
        return self.pendulum_dt.to_date_string()

    @property
    def time(self) -> str:
        """Returns the time the task was created"""
        return self.pendulum_dt.to_time_string()

    @property
    def datetime(self) -> str:
        """Returns the full datetime the issue was created"""
        return self.pendulum_dt.to_datetime_string()


class Gmail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_address = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    thread_id = models.CharField(max_length=50, unique=True)


class TaskAddonProvider(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=40)
    color = models.CharField(max_length=8)
    shortcut = models.CharField(max_length=10, null=True, blank=True)
    base_url = models.URLField()

    @staticmethod
    def get_absolute_url() -> str:
        """Returns the list url of the model."""
        return reverse("prod:providers_list")

    def __str__(self):
        """Returns the representation string for the model."""
        return self.name

    def show_base_url(self, task):
        """Renders the template url into the file link."""
        return self.base_url.format(task=task)

    def remove_hex_prefix(self):
        """Removes the # on colors"""
        self.color = self.color.replace("#", "")


class TaskAddon(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    provider = models.ForeignKey(TaskAddonProvider, on_delete=models.CASCADE)
    uid = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.provider.name + ' for ' + self.task.__str__()

    def set_params(self) -> None:
        if self.url:
            self.uid = self.url.split('/')[-1]
        if self.uid and self.provider and not self.url:
            self.url = self.provider.show_base_url(self.task) + self.uid
        self.save()


@receiver(post_save, sender=Task)
def create_task_addon(sender, instance, created, **kwargs):
    if instance.has_addon_in_task() and instance.project:
        instance.extract_addons()


@receiver(post_save, sender=TaskAddon)
def set_addon_url(sender, instance, created, **kwargs):
    if created:
        instance.set_params()


@receiver(pre_save, sender=TaskAddonProvider)
@receiver(pre_save, sender=Project)
def removes_prefix_from_colors(sender, instance, **kwargs):
    instance.remove_hex_prefix()
