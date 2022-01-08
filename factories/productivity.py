import pendulum
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyChoice


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.Category'
        django_get_or_create = ('name')

    name = FuzzyText(length=20)
    emoji = FuzzyChoice(choices=['✅', '❓', '👔', '❌', '👀'])
    todoist_id = FuzzyInteger(low=10_000)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create(*args, **kwargs)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.Project'
        django_get_or_create = ('name')

    name = FuzzyText(length=20)
    color = Faker('color')
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create(*args, **kwargs)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.Task'

    created_at = pendulum.now()
    category = SubFactory(CategoryFactory)
    task = FuzzyText(length=100)
    project = SubFactory(ProjectFactory)
    todoist_id = FuzzyInteger(low=100_000)


class GmailFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.Gmail'
        django_get_or_create = ('thread_id',)

    from_address = Faker('free_email')
    subject = FuzzyText(length=300)
    done = FuzzyChoice((True, False))
    thread_id = FuzzyText(length=45)


class TaskAddonProviderFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.TaskAddonProvider'
        django_get_or_create = ('name',)

    name = Faker('company')
    icon = FuzzyText(length=40)
    color = Faker('color')
    shortcut = FuzzyText(length=10)
    base_url = Faker('image_url')


class TaskAddonFactory(DjangoModelFactory):
    class Meta:
        model = 'productivity.TaskAddon'
        django_get_or_create = ('provider', 'uid')

    task = SubFactory(TaskFactory)
    provider = SubFactory(TaskAddonProviderFactory)
    uid = FuzzyText(length=50)
    url = str(Faker('image_url')) + "{task}"
