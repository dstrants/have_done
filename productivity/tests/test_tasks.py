import json

import pytest
from django.contrib.auth.models import AnonymousUser

from factories.productivity import (CategoryFactory, ProjectFactory,
                                    TaskAddonProviderFactory, TaskFactory)
from factories.user import AdminUser
from productivity import views
from productivity.models import Task


@pytest.mark.django_db
class TestTasks:
    """Tests regarding the `productivity.models.Tasks` mdoe and views."""
    @staticmethod
    def test_home_view(rf):
        """Validates home view rendering."""
        request = rf.get("/")
        request.user = AdminUser()
        response = views.home(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_unauthenticated_view(rf):
        """Anonymous users should be redirected."""
        request = rf.get("/")
        request.user = AnonymousUser()
        response = views.home(request)

        assert response
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=/'

    @staticmethod
    def test_today_view(rf):
        """Validates today's view rendering."""
        request = rf.get("/productivity/today")
        request.user = AdminUser()
        response = views.today(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_weekly_no_weekno_view(rf):
        """Weekly view rendering for this week."""
        request = rf.get("/productivity/week/")
        request.user = AdminUser()
        response = views.this_week(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_weekly_with_weekno_view(rf):
        """Weekly view rendering with a given week number."""
        request = rf.get("/productivity/week/?week_no=12")
        request.user = AdminUser()
        response = views.this_week(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_weekly_with_faulty_weekno_view(rf):
        """Weekly view with invalid week number should fail."""
        request = rf.get("/productivity/week?week_no=158")
        request.user = AdminUser()
        response = views.this_week(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_tasks_refresh_view(rf):
        """Tasks list partial rendering."""
        request = rf.get("/productivity/today/refresh")
        request.user = AdminUser()
        response = views.tasks_today(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_tasks_refresh_with_date_view(rf):
        """Tasks list partial for a given day."""
        request = rf.get("/productivity/today/refresh?date=2020-04-04")
        request.user = AdminUser()
        response = views.tasks_today(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_task_creation(rf):
        """Task creation view."""
        count = Task.objects.count()
        cat, pro = CategoryFactory(), ProjectFactory()
        request = rf.post(f"/productivity/tasks/create?cat_id={cat.id}&pro={pro.id}&name=adsfasdfasdfasdasd")
        request.user = AdminUser()
        response = views.create_task(request)

        assert response
        assert response.status_code == 302

        assert count + 1 == Task.objects.count()

    @staticmethod
    def test_task_creation_missing_project(rf):
        """Task without project should fail."""
        cat = CategoryFactory()
        request = rf.post(f"/productivity/tasks/create?cat_id={cat.id}&name=adsfasdfasdfasdasd")
        request.user = AdminUser()
        response = views.create_task(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_task_creation_missing_category(rf):
        """Task without category should fail."""
        pro = ProjectFactory()
        request = rf.post(f"/productivity/tasks/create?pro={pro.id}&name=adsfasdfasdfasdasd")
        request.user = AdminUser()
        response = views.create_task(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_task_creation_missing_name(rf):
        """Task with missing name should fail."""
        cat, pro = CategoryFactory(), ProjectFactory()
        request = rf.post(f"/productivity/tasks/create?cat_id={cat.id}&pro={pro.id}")
        request.user = AdminUser()
        response = views.create_task(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_task_creation_get_view(rf):
        """Creating task with `GET` should fail."""
        cat, pro = CategoryFactory(), ProjectFactory()
        request = rf.get(f"/productivity/tasks/create?cat_id={cat.id}&pro={pro.id}&name=adsfasdfasdfasdasd")
        request.user = AdminUser()
        response = views.create_task(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_task_deletion_view(rf):
        """Checks task deletion view."""
        task = TaskFactory()
        request = rf.post(f"/productivity/tasks/delete?task={task.id}")
        request.user = AdminUser()
        response = views.delete_task(request)

        assert response
        assert response.status_code == 200

        body = json.loads(response.content)

        assert 'message' in body

        assert not Task.objects.filter(id=task.id).exists()

    @staticmethod
    def test_task_deletion_with_get_view(rf):
        """Deleting a task through `GET` should fail."""
        task = TaskFactory()
        request = rf.get(f"/productivity/tasks/delete?task={task.id}")
        request.user = AdminUser()
        response = views.delete_task(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_non_existing_task_deletion_view(rf):
        """Deleting a task that does not exist should fail."""
        task = TaskFactory()
        request = rf.post(f"/productivity/tasks/delete?task={task.id + 15_000}")
        request.user = AdminUser()
        response = views.delete_task(request)

        assert response
        assert response.status_code == 404

    @staticmethod
    def test_task_fast_update_view_html(rf):
        """Validates the rendering of fast update view."""
        task = TaskFactory()
        request = rf.get(f"/productivity/task/{task.id}/list")
        request.user = AdminUser()
        response = views.task_text_fast_update_view(request, task=task.id)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_task_fast_update_project(rf):
        """Testing project fast update for task."""
        task = TaskFactory()
        new_pro = ProjectFactory(name='new-project')

        request = rf.post(f"/productivity/task/fu/{task.id}/project_id/{new_pro.id}")
        request.user = AdminUser()
        response = views.task_fast_update(request, task=task.id, field='project_id', val=new_pro.id)

        assert response
        assert response.status_code == 200
        body = json.loads(response.content)

        assert body['result']
        assert 'message' in body

        task = Task.objects.get(id=task.id)

        assert task
        assert task.project == new_pro

    @staticmethod
    def test_task_fast_update_category(rf):
        """Testing category fast update for task."""
        task = TaskFactory()
        new_cat = CategoryFactory(name='new-category')

        request = rf.post(f"/productivity/task/fu/{task.id}/category_id/{new_cat.id}")
        request.user = AdminUser()
        response = views.task_fast_update(request, task=task.id, field='category_id', val=new_cat.id)

        assert response
        assert response.status_code == 200
        body = json.loads(response.content)

        assert body['result']
        assert 'message' in body

        task = Task.objects.get(id=task.id)

        assert task
        assert task.category == new_cat

    @staticmethod
    def test_task_fast_update_text(rf):
        """Testing text fast update for task."""
        task = TaskFactory()
        new_task = "Threre something else to be done!"

        request = rf.post(f"/productivity/task/fu/{task.id}/task/{new_task.encode()}")
        request.user = AdminUser()
        response = views.task_fast_update(request, task=task.id, field='task', val=new_task)

        assert response
        assert response.status_code == 200
        body = json.loads(response.content)

        assert body['result']
        assert 'message' in body

        task = Task.objects.get(id=task.id)

        assert task
        assert task.task == new_task

    @staticmethod
    def test_task_fast_update_get(rf):
        """Test fast update with `GET` should fail."""
        task = TaskFactory()
        new_task = "It should not work"

        request = rf.get(f"/productivity/task/fu/{task.id}/task/{new_task.encode()}")
        request.user = AdminUser()
        response = views.task_fast_update(request, task=task.id, field='task', val=new_task)

        assert response
        assert response.status_code == 400

        fresh_task = Task.objects.get(id=task.id)

        # Nothing should have changed
        assert fresh_task
        assert fresh_task.task == task.task
        assert fresh_task.project == task.project
        assert fresh_task.category == task.category

    @staticmethod
    def test_task_fast_update_invalid_field(rf):
        """Fast update with invalid field should fail."""
        task = TaskFactory()
        new_task = "It should not work as well!"

        request = rf.post(f"/productivity/task/fu/{task.id}/task/{new_task.encode()}")
        request.user = AdminUser()
        response = views.task_fast_update(request, task=task.id, field='tasl', val=new_task)

        assert response
        assert response.status_code == 200

        body = json.loads(response.content)

        assert not body['result']
        assert 'message' in body

        fresh_task = Task.objects.get(id=task.id)

        # Nothing should have changed
        assert fresh_task
        assert fresh_task.task == task.task
        assert fresh_task.project == task.project
        assert fresh_task.category == task.category

    @staticmethod
    def test_task_model_str():
        """Validates `Task.__str__`."""
        task = TaskFactory()

        assert task.__str__() == task.category.emoji + task.task

    @staticmethod
    def test_task_mode_extract_non_existing_addon():
        """Tests the handling of non existing addon param inside task field."""
        task = TaskFactory(task='This is a task with non existing addon todi:145')

        assert task.task
        # No addon created
        assert task.taskaddon_set.count() == 0
        # The reduntant string has been removed
        assert 'todi:145' not in task.task

    @staticmethod
    def test_task_null_addon_creation():
        """Tests handling existing addon without value."""
        todoist = TaskAddonProviderFactory(name='todoist', shortcut='todoist')
        assert todoist

        task = TaskFactory(task='I am creating a task with null addon value todoist:  ')

        assert task
        assert task.taskaddon_set.count() == 0
        assert 'todoist:' not in task.task

    @staticmethod
    def test_task_http_addon_creation():
        """Tests creating addon with link as uid."""
        todoist = TaskAddonProviderFactory(name='todoist', shortcut='todoist')
        assert todoist

        task = TaskFactory(task='I am creating a task with http value todoist:https://todoist.com/1234')

        assert task
        assert task.taskaddon_set.count() == 1
        assert 'todoist:https://todoist.com/1234' not in task.task

        assert task.taskaddon_set.first().url == "https://todoist.com/1234"

    @staticmethod
    def test_tasks_on_default_project_does_not_exist_view(rf):
        """Validates defaults redirects when default project does not exists."""
        request = rf.get("/productivity/defaults")
        request.user = AdminUser()
        response = views.tasks_in_default(request)

        assert response
        assert response.status_code == 302

    @staticmethod
    def test_tasks_on_default_project_view(rf):
        ProjectFactory(name='default')
        request = rf.get("/productivity/defaults")
        request.user = AdminUser()
        response = views.tasks_in_default(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_tasks_on_default_project_does_not_exist(rf):
        """Tests that 404 is returned when default project does not exist."""
        request = rf.get("/productivity/tasks/project/default")
        request.user = AdminUser()
        response = views.find_by_project(request, pro='default')

        assert response
        assert response.status_code == 404

    @staticmethod
    def test_tasks_on_default_project_partial(rf):
        """Tests that 404 is returned when default project does not exist."""
        pro = ProjectFactory(name='default')
        for i in range(10):
            TaskFactory(task=f"task {i}", project=pro)
        request = rf.get("/productivity/tasks/project/default")
        request.user = AdminUser()
        response = views.find_by_project(request, pro='default')

        assert response
        assert response.status_code == 200
