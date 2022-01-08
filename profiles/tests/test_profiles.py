import json

import pytest
from factory.django import ImageField

from factories.profiles import ProfileFactory
from profiles.models import Profile
from profiles.views import AvatarUpdateview, refresh_token


@pytest.mark.django_db
class TestProfile:
    """Tests regarding the `profile.models.Profile` model."""
    @staticmethod
    def test_avatar_update_get_view(rf):
        """Validates the rendering of avatar update view."""
        profile = ProfileFactory()
        request = rf.get("/profiles/avatar/")
        request.user = profile.user
        response = AvatarUpdateview.as_view()(request)

        assert response
        assert response.status_code == 200

    # TODO: Find a way to test the avatar upload form
    @pytest.mark.skip(reason="ImageFields are keep beeing marked as None on local dev.")
    @staticmethod
    def test_avatar_update_post_view(rf):
        """Tests the image update view."""
        profile = ProfileFactory()
        new_image = ImageField(from_path='media/favicon.png', file_name='test_image2.jpeg')
        request = rf.post("/profiles/avatar/", {'avatar': new_image})
        request.user = profile.user
        response = AvatarUpdateview.as_view()(request)

        assert response
        assert response.status_code == 302

        prof = Profile.objects.get(id=profile.id)
        assert prof
        assert prof.avatar

    @staticmethod
    def test_refresh_token_view(rf):
        """Tests the refresh token view."""
        profile = ProfileFactory()
        tkn = profile.token
        request = rf.get("/profiles/refresh_token")
        request.user = profile.user
        response = refresh_token(request)

        assert response
        assert response.status_code == 200

        content = json.loads(response.content.decode())
        assert content['token']

        prof = Profile.objects.get(id=profile.id)
        assert prof.token
        assert prof.token.key == content['token'] != tkn

    @staticmethod
    def test_profile_str():
        """Validates the `Profile.__str__`'"""
        profile = ProfileFactory()

        assert str(profile) == profile.user.username

    @staticmethod
    def test_profile_token_property():
        """Validates the `Profile.token` property."""
        profile = ProfileFactory()

        # Token should be None by default
        assert profile.token is None

        token = profile.refresh_api_token()

        assert token == profile.token

    @staticmethod
    def test_profile_refresh_token_deletion():
        """Validates tha the token is being refreshed."""
        profile = ProfileFactory()

        initial_token = profile.refresh_api_token()

        profile.refresh_api_token()

        assert profile.token != initial_token

    @staticmethod
    def test_profile_usa_method():
        """Validates the `Profile.has_usa('provider')` method."""
        profile = ProfileFactory()

        assert profile.has_usa('google') is None

        from social_django.models import UserSocialAuth

        usa = UserSocialAuth.objects.create(user=profile.user, provider='google')

        assert usa
        assert profile.has_usa('google') == usa
