import pytest


@pytest.fixture
def todoist_task() -> dict:
    """A valid todoist task. (Taken from api docs)."""
    return {
        "id": 301946961,
        "legacy_id": 33511505,
        "user_id": 1855589,
        "project_id": 396936926,
        "legacy_project_id": 128501470,
        "content": "**task1** with some `code`",
        "priority": 1,
        "due": None,
        "parent_id": None,
        "legacy_parent_id": None,
        "child_order": 1,
        "section_id": None,
        "day_order": -1,
        "collapsed": 0,
        "children": None,
        "labels": [12839231, 18391839],
        "added_by_uid": 1855589,
        "assigned_by_uid": 1855589,
        "responsible_uid": None,
        "checked": 0,
        "in_history": 0,
        "is_deleted": 0,
        "sync_id": None,
        "date_added": "2014-09-26T08:25:05Z"
    }
