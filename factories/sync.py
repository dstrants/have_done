import pendulum

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyInteger, FuzzyText, FuzzyChoice
from factories.productivity import ProjectFactory


class PullRequestFactory(DjangoModelFactory):
    class Meta:
        model = 'sync.PullRequest'
        django_get_or_create = ('number', 'repo_full_name')

    number = FuzzyInteger(low=1)
    html_url = Faker('image_url')
    title = FuzzyText(prefix='PR: ', length=25)
    opened_by = f"{Faker('first_name')}_{Faker('last_name')}"
    user_url = Faker('image_url')
    repo_name = Faker('lexify', text='????????')
    repo_full_name = Faker('lexify', text='????????/????????')
    private = FuzzyChoice((True, False))
    created_at = FuzzyDateTime(
        start_dt=pendulum.now().subtract(months=1),
        end_dt=pendulum.now().subtract(weeks=2)
    )
    updated_at = FuzzyDateTime(start_dt=pendulum.now().subtract(weeks=2))


class RepositoryFactory(DjangoModelFactory):
    class Meta:
        model = 'sync.Repository'
        django_get_or_create = ('name',)

    name = Faker('microservice')
    project = SubFactory(ProjectFactory)
