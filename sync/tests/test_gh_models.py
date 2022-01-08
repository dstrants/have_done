import pytest
from django.db import IntegrityError

from factories.sync import PullRequestFactory, RepositoryFactory
from sync.models import PullRequest


@pytest.mark.django_db
class TestLogsModels:
    @staticmethod
    def test_pull_request_str():
        """Checks the basic rules for a pull request."""
        pr = PullRequestFactory(private=True)
        assert pr.id is not None
        assert pr.status
        assert pr.private
        assert pr.__str__() == f"{pr.title} from {pr.repo_name}"

    @staticmethod
    def test_pull_request_unique():
        """Validates that the combination of pr.number and pr.repo_name is unique."""
        pr = PullRequestFactory(number=48897, repo_name='rails')

        assert pr

        with pytest.raises(IntegrityError):
            # has to be manually created as Factory user get_or_create
            PullRequest.objects.create(
                number=48897, repo_name='rails'
            )

    @staticmethod
    def test_repository_str():
        """Tests the creation of repository model."""
        repo = RepositoryFactory(name='backups')
        assert repo.id is not None
        assert repo.project is not None
        assert repo.__str__() == 'backups'
