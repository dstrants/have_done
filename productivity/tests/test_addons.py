import pytest
from django.db import IntegrityError
from django.test import RequestFactory

from factories.productivity import (TaskAddonFactory, TaskAddonProviderFactory,
                                    TaskFactory)
from factories.user import AdminUser
from productivity.models import TaskAddon
from productivity.views import add_new_addon


@pytest.mark.django_db
class TestAddons:
    """Tests regarding the `productivity.models.TaskAddon`."""
    @staticmethod
    def test_create_task_addon(rf: RequestFactory) -> None:
        """Tests the functinality of taskm addon creation view."""
        task = TaskFactory()
        provider = TaskAddonProviderFactory()
        request = rf.post(f'/prod/task/{task.id}/addon',
                          {'pid': provider.id, 'uid': 25})
        request.user = AdminUser()
        cnt = TaskAddon.objects.count()
        response = add_new_addon(request, task.id)
        addon = TaskAddon.objects.get(task=task, uid=25, provider=provider)
        assert addon
        assert TaskAddon.objects.count() == cnt + 1
        assert addon in task.taskaddon_set.all()
        assert response.status_code == 302

    @staticmethod
    def test_create_task_addon_with_uid(rf: RequestFactory) -> None:
        """Checks the addon creation with link as uid."""
        task = TaskFactory()
        provider = TaskAddonProviderFactory()
        request = rf.post(f'/prod/task/{task.id}/addon',
                          {'pid': provider.id, 'uid': 'https://provider.page.com/test/123'})
        request.user = AdminUser()
        cnt = TaskAddon.objects.count()
        response = add_new_addon(request, task.id)
        addon = TaskAddon.objects.get(task=task, uid=123, provider=provider)
        assert addon
        assert TaskAddon.objects.count() == cnt + 1
        assert addon in task.taskaddon_set.all()
        assert addon.uid == '123'
        assert response.status_code == 302

    @staticmethod
    def test_get_task_addon_partial(rf: RequestFactory) -> None:
        """Checks the task addon partial rendering."""
        task = TaskFactory()
        total_addons = TaskAddon.objects.count()
        request = rf.get(f'/prod/task/{task.id}/addon')
        request.user = AdminUser()
        response = add_new_addon(request, task.id)
        assert response.status_code == 200
        assert total_addons == TaskAddon.objects.count()

    @staticmethod
    def test_task_addon_task_null():
        """TaskAddon.task can't be null."""
        with pytest.raises(IntegrityError):
            TaskAddonFactory(provider=None)

    @staticmethod
    def test_task_addon_provider_null():
        """TaskAddon.task can't be null."""
        with pytest.raises(IntegrityError):
            TaskAddonFactory(task=None)

    @staticmethod
    def test_addon_url_generation():
        """Checks if url is generated from uid."""
        addon = TaskAddonFactory(url=None)
        assert addon.url not in (None, "", "")
        assert addon.url == addon.provider.base_url.format(task=addon.task) + addon.uid

    @staticmethod
    def test_addon_uid_generation():
        """Checks if uid is generated from url."""
        addon = TaskAddonFactory(url="https://github.com/415")
        assert addon.uid not in (None, "", "")
        assert addon.uid == addon.url.split("/")[-1]

    @staticmethod
    def test_addon_str():
        """Validates the format of `TaskAddon.__str__()`."""
        addon = TaskAddonFactory()

        assert addon.__str__() == f"{addon.provider.name} for {addon.task.__str__()}"
