import pytest

from factories.user import UserFactory


@pytest.mark.django_db
class TestLogsImporters:
    """Test regarding the logs.importerts helper file."""
    @staticmethod
    def test_user_with_social_auth() -> None:
        """
        Tests the social auth user key fuctionality
        """
        data = {'access_token': 'asdfasdfasdfasdfasd'}
        user = UserFactory(username='testuser', password='iamatestuser')
        user.social_auth.create(provider='github', extra_data=data)

        # Asserts it returns a key string
        assert user.profile.access_token('github') == 'asdfasdfasdfasdfasd'

        # Deletes the social auth model
        user.social_auth.all().delete()

        # Should return None
        assert not user.profile.access_token('github')
