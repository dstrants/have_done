import pytest

from factories.productivity import TaskAddonProviderFactory
from factories.user import AdminUser
from productivity.models import TaskAddonProvider
from productivity.views import (CreateAddonProviderView, ListAddonProviderView,
                                UpdateAddonProviderView)

# TAP == TaskAddonProvider


@pytest.mark.django_db
class TestTaskAddonProviders:
    """Testing the model and views of `productivity.models.TaskAddonProviderz."""
    @staticmethod
    def test_create_tap_get_view(rf):
        """Tests the provider creation view rendering."""
        request = rf.get("/productivity/providers/create")
        request.user = AdminUser()
        response = CreateAddonProviderView.as_view()(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_create_tap_post_view(rf):
        """Test the creation of new provider through the creation view."""
        data = {
            'name': 'SimpleProvider',
            'icon': 'todoist',
            'color': '#008ed6',
            'shortcut': 'todoist',
            'base_url': 'https://todoist.com/{task}'
        }
        cnt = TaskAddonProvider.objects.count()
        request = rf.post("/productivity/providers/create", data)
        request.user = AdminUser()
        response = CreateAddonProviderView.as_view()(request)

        assert response
        assert response.status_code == 302
        assert cnt + 1 == TaskAddonProvider.objects.count()

        provider = TaskAddonProvider.objects.get(name='SimpleProvider')

        assert provider
        assert provider.icon == 'todoist'
        assert provider.color == '008ed6'
        assert provider.shortcut == 'todoist'
        assert provider.base_url == 'https://todoist.com/{task}'

    @staticmethod
    def test_list_tap_view(rf):
        """Test list view for providers."""
        request = rf.get("/productivity/providers/")
        request.user = AdminUser()
        response = ListAddonProviderView.as_view()(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_update_tap_post_view(rf):
        """Test providers update view."""
        data = {
            'name': 'SimplestProvider',
            'icon': 'todoist',
            'color': '#008ed6',
            'shortcut': 'todoist',
            'base_url': 'https://todoist.com/{task}'
        }
        provider = TaskAddonProviderFactory(**data)
        cnt = TaskAddonProvider.objects.count()
        request = rf.post(f"/productivity/providers/update/{provider.id}", data)
        request.user = AdminUser()
        response = UpdateAddonProviderView.as_view()(request, pk=provider.id)

        assert response
        assert response.status_code == 302
        assert cnt == TaskAddonProvider.objects.count()

        provider = TaskAddonProvider.objects.get(name='SimplestProvider')

        assert provider
        assert provider.icon == 'todoist'
        assert provider.color == '008ed6'
        assert provider.shortcut == 'todoist'
        assert provider.base_url == 'https://todoist.com/{task}'

    @staticmethod
    def test_tap_str():
        """Validates the `TaskAddonProvider.__str__`."""
        provider = TaskAddonProviderFactory()

        assert provider.__str__() == provider.name
