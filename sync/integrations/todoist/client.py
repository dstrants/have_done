from typing import List, Optional

import todoist
from django.contrib.auth.models import User
from pydantic import ValidationError

from productivity.models import Project
from sync.decorators import token
from sync.integrations.todoist.validators import (TodoistItem, TodoistLabel,
                                                  TodoistProject)


class TodoistClient():

    def __init__(self, user) -> None:
        self.user: User = user
        self.key: Optional[str] = self._set_api_key()
        self.api: Optional[todoist.TodoistAPI] = self._set_api()

    def _set_api_key(self) -> Optional[str]:
        """Locates the todoist api key for the user, if any."""
        if usa := self.user.social_auth.get(provider='todoist'):
            return usa.extra_data['access_token']
        return None

    @token
    def _set_api(self) -> Optional[todoist.TodoistAPI]:
        """Instantiates the todoistAPI on the class."""
        api = todoist.TodoistAPI(self.key)
        api.sync()
        return api

    @token
    def fetch_projects(self) -> Optional[list]:
        """Fetches the projects from todoist Api."""
        return list(self.api.state['projects'])

    @token
    def projects(self) -> Optional[List[TodoistProject]]:
        """Returns a validated list of TodoistTasks."""
        projects = []
        for pro in self.fetch_projects():
            try:
                projects.append(TodoistProject(**pro.data))
            except ValidationError:
                print(f"Could not validate \n {pro}")
        return projects

    @token
    def fetch_labels(self) -> Optional[list]:
        """Fetches labels from the api."""
        return list(self.api.state['labels'])

    @token
    def labels(self) -> Optional[List[TodoistLabel]]:
        """Returns a set of TodoistLabel."""
        labels = []
        for lab in self.fetch_labels():
            try:
                labels.append(TodoistLabel(**lab.data))
            except ValidationError:
                print(f"Could not validate \n {lab}")
        return labels

    @token
    def fetch_completed_tasks(self) -> Optional[list]:
        """fetches completed data from the api."""
        items = []
        for project in Project.active.filter(todoist_id__isnull=False):
            items.append(self.api.items.get_completed(project.todoist_id))
        return items

    def completed_tasks(self) -> List[TodoistItem]:
        """Returns the full list of completed tasks."""
        tasks = []
        for project in self.fetch_completed_tasks():
            for item in project:
                try:
                    task = TodoistItem(**item)
                except ValidationError:
                    print(f"Could not validate \n {item}")
                else:
                    tasks.append(task)
        return tasks
