import logging
from typing import Optional

from pymongo import MongoClient
from pydantic import BaseModel

from django.conf import settings

from productivity.models import Category, Project, Task


logger = logging.getLogger(__name__)
COLORS = [
    "#b8256f", "#db4035", "#ff9933", "#fad000", "#afb83b", "#7ecc49", "#299438", "#6accbc",
    "#158fad", "#14aaf5", "#96c3eb", "#4073ff", "#884dff", "#af38eb", "#eb96eb", "#e05194",
    "#ff8d85", "#808080", "#b8b8b8", "#ccac93"
    ]


class DueDate(BaseModel):

    date: str
    timezone: Optional[str]
    string: str
    lang: str
    is_recurring: bool


class TodoistItem(BaseModel):

    id: int
    content: str
    checked: bool
    project_id: int
    description: Optional[str] = None
    user_id: int
    in_history: int
    priority: int
    collapsed: int
    date_added: str
    date_completed: Optional[str]
    assigned_by_uid: Optional[int]
    responsble_by_uid: Optional[int]
    added_by_uid: Optional[int]
    is_deleted: bool
    sync_id: Optional[int]
    parent_id: Optional[int]
    child_order: Optional[int]
    section_id: Optional[int]
    labels: list
    notes: Optional[list]
    due: Optional[DueDate]

    def _project(self) -> Optional[Project]:
        """Returns a list of local projects that are linked to a todoist project."""
        if projects := Project.todoist.filter(todoist_id=self.project_id):
            return projects.first()
        return None

    def _category(self) -> Optional[Category]:
        """Returns a list of local projects that are linked to a todoist labels."""
        if not (labels := self.labels):
            # TODO: implement a default category
            return Category.objects.filter(name__icontains='task').first()

        if cats := Category.todoist.filter(todoist_id__in=labels):
            return cats.first()
        return None

    def _addon_str(self) -> str:
        """Returns the string to be used for creating the task addon."""
        return f" todoist:{self.id}"

    def _backup_task(self) -> str:
        """
        Returns the task content in the needed format including
        the relative addon text.
        """
        return self.content + self._addon_str()

    def _params(self) -> Optional[dict]:
        """
        Returns a parameters dict that translates todoist task attributes
        to local task attributes.
        """
        if not ((project := self._project()) and (cat := self._category())):
            return None
        return {
            'task': self._backup_task(),
            'project': project,
            'category': cat,
            'todoist_id': self.id,
            'created_at': self.date_completed
        }

    def exists(self) -> bool:
        """Checks if a local task related to self todoist task exists."""
        return Task.objects.filter(todoist_id=self.id).exists()

    def save(self) -> Optional[Task]:
        """Creates a local task based on the self todoist task if possible.

        Returns None if the task already exists (based on todoist id).
        Returns None if params could not be built.
        Returns None if the task could not be saved.
        Returns the Task instance if it was successfully created.
        """

        if self.exists():
            logger.info("Task for todoist item %s already exists, skipping task creation...", self.id)
            return None

        if not (params := self._params()):
            msg = "Local project or category not in watchlist for todoist task %s. Check configuration. Skipping task creation..." #noqa
            logger.warning(msg, self.id)

        try:
            task = Task.objects.create(**params)
            logger.info("Task from todoist item %s created. TaskId: #%s", self.id, task.id)
        except:
            return None
        return task

    def save_to_mongo(self) -> object:
        client = MongoClient(settings.MONGO_CONNECTION_STRING)
        tasks = client.backups.todoist_items
        if not tasks.find_one({"id": self.id}):
            tasks.insert_one(self.dict())
            logger.info("Saving todoist task %s to mongo", self.id)
        else:
            logger.info("Task already exists in mongo. Skipping save to db.")

        return self


class TodoistProject(BaseModel):

    child_order: int
    collapsed: bool
    color: int
    has_more_notes: bool
    id: int
    inbox_project: bool = False
    is_archived: bool
    is_deleted: bool
    is_favorite: bool
    name: str
    parent_id: Optional[int]
    shared: bool
    sync_id: Optional[int]

    def color_hex(self) -> str:
        """Returns the color of the self todoist project."""
        return COLORS[self.color - 30]


class TodoistLabel(BaseModel):

    color: int
    id: int
    is_deleted: bool
    is_favorite: bool
    item_order: int
    name: str

    def color_hex(self) -> str:
        """Returns the color of the self todoist label."""
        return COLORS[self.color - 30]


class TodoistWebhookInitiator(BaseModel):
    email: str
    full_name: str
    id: str
    image_id: Optional[str]
    is_premium: bool


class TodoistWebhook(BaseModel):
    event_name: str
    user_id: int
    event_data: TodoistItem
    initiator: TodoistWebhookInitiator
    version: str
