import pytest

from factories.productivity import (CategoryFactory, ProjectFactory,
                                    TaskAddonProviderFactory)
from sync.integrations.todoist.validators import TodoistItem


@pytest.mark.django_db
class TestTodoistValidator:

    @staticmethod
    def test_valid_item(todoist_task: dict):
        """
        Checks that validation passes on a valid task
        """
        assert TodoistItem(**todoist_task)

    @staticmethod
    def test_addon_render(todoist_task: dict):
        """
        Checks that the validator creates tht task addon
        string properly.
        """
        task = TodoistItem(**todoist_task)
        assert ' todoist:301946961' == task._addon_str()

    @staticmethod
    def test_task_task_render(todoist_task: dict):
        """
        Checks that the whole Task.task is rendered
        properly from the validator
        """
        task = TodoistItem(**todoist_task)
        assert '**task1** with some `code` todoist:301946961' == task._backup_task()

    @staticmethod
    def test_task_project_location(db, todoist_task: dict):
        """
        Checks that the validator can locate the backups
        project of the task.
        """
        project = ProjectFactory(todoist_id=396936926)
        task = TodoistItem(**todoist_task)
        assert task._project() == project

    @staticmethod
    def test_task_category_location(db, todoist_task: dict):
        """
        Checks that the validator can locate the backups
        category of the task.
        """
        ProjectFactory(todoist_id=396936926)
        category = CategoryFactory(todoist_id=12839231)
        task = TodoistItem(**todoist_task)
        assert task._category() == category

    @staticmethod
    def test_task_save(db, todoist_task: dict):
        """
        Checks that a valid todoist task is properly saved to db
        """
        TaskAddonProviderFactory(name='Todoist', shortcut='todoist')
        project = ProjectFactory(todoist_id=396936926)
        category = CategoryFactory(todoist_id=12839231)
        task = TodoistItem(**todoist_task)
        db_task = task.save()
        assert db_task is not None
        assert db_task.project == project
        assert db_task.category == category
        assert db_task.taskaddon_set.count() > 0
