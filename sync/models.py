from django.contrib.auth.models import User
from django.db import models

from productivity.models import Category, Project, Task


class Sync(models.Model):
    """Implements the Sync job logging model"""
    INTEGRATIONS = [(0, 'Todoist'), (1, 'Google'), (2, 'Github')]
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    integration = models.IntegerField(choices=INTEGRATIONS)
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, verbose_name='syncs', on_delete=models.CASCADE)


class PullRequest(models.Model):
    """Model that represents gh prs"""
    number = models.IntegerField()
    html_url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=400, default='Pull Request')
    opened_by = models.CharField(max_length=300, default='gh-user')
    user_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=50, default='open')
    repo_name = models.CharField(max_length=100)
    repo_full_name = models.CharField(max_length=200)
    private = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    merged_at = models.DateTimeField(blank=True, null=True)
    task_created = models.BooleanField(default=False)

    def create_task(self) -> None:
        """Creates a Task for a merged PR"""
        if self.task_created:
            return None

        cat = Category.objects.get(name="task")
        pro = Project.objects.get(name='default')

        try:
            repo = Repository.objects.get(name=self.repo_full_name)
        except Repository.DoesNotExist:
            pass
        else:
            if repo.project:
                pro = repo.project

        Task.objects.create(
            category=cat,
            project=pro,
            task=f"**Merged PR** -> *{self.title}* at `{self.repo_full_name}` gh:{self.html_url}"
        )
        self.task_created = True
        return None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        """Overrides the default method to check if a task must be created.

        NOTE: New task needs to be created only for newly merged PRs
        """
        check = False
        if not (
            old := PullRequest.objects.filter(pk=getattr(self, "pk", None)).first()
        ):
            check = True
        elif old.status != self.status:
            check = True

        if check and self.status == 'closed' and self.merged_at:
            self.create_task()

        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    def __str__(self):
        return self.title + ' from ' + self.repo_name

    class Meta:
        unique_together = ['number', 'repo_name']


class Repository(models.Model):
    """Implements the model repository"""
    name = models.CharField(max_length=200, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="repos")
    private = models.BooleanField(default=False)
    watch = models.BooleanField(default=False)

    class Meta:
        ordering = ('-watch', 'name')

    def __str__(self):
        return self.name

    @property
    def link(self) -> str:
        return f"https://github.com/{self.name}"
