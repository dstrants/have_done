import pytest

from factories.profiles import ProfileSettingFactory
from profiles.models import ProfileSetting
from profiles.views import SettingsView


@pytest.mark.django_db
class TestProfileSettings:
    """Tests regaring the `profiles.models.ProfileSetting`."""
    @staticmethod
    def test_update_settings_get_view(rf):
        """Validates rendering of settings update view."""
        sets = ProfileSettingFactory()
        request = rf.get("/profiles/settings")
        request.user = sets.profile.user
        response = SettingsView.as_view()(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_update_settings_post_view(rf):
        """Tests updating of settings."""
        sets = ProfileSettingFactory(gmail=True)
        sets.gmail = True
        sets.save(update_fields=['gmail'])

        assert sets.gmail

        request = rf.post("/profiles/settings/", {'gmail': False})
        request.user = sets.profile.user
        response = SettingsView.as_view()(request)

        assert response
        assert response.status_code == 302

        assert not sets.gmail

        # Load from db as well
        settings = ProfileSetting.objects.get(id=sets.id)

        assert not settings.gmail

    @staticmethod
    def test_profile_settings_str():
        """Validates the `ProfileSetting.__str__`."""
        settings = ProfileSettingFactory()

        assert settings
        assert f"Settings for: {settings.profile.user.username}"
