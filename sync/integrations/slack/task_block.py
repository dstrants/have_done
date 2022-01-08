import pendulum
from productivity.models import Task

TODAY_LINK = "https://backups.p.strdi.me/prod/today/"
DAILY_TASK_REPORT_TEMPLATE = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "emoji": True,
            "text": "Here are the tasks to report today:"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*<{TODAY_LINK}?date={pendulum.yesterday().to_date_string()}|Check Out>*"
        },
    },
    {
        "type": "divider"
    },
]

MESSAGE_BLOCK = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":warning: Looks like you have not logged any tasks today:"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*<{TODAY_LINK}|Add now>*"
        }
    },
]


class TaskBlock:
    def __init__(self, task: Task) -> None:
        self.task: Task = task

    def task_block(self) -> dict:
        """Renders a message block for the slack notifications"""
        body = f"{self.task.category.emoji} *{self.task.task}* #{self.task.project.name}"
        addons = ",".join((f"<{addon.url}|{addon.provider.name}>" for addon in self.task.taskaddon_set.all()))
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{body}\n{addons}"
            }
        }
