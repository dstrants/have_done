from dramatiq import actor, get_broker
from periodiq import PeriodiqMiddleware, cron

from productivity.models import Project, Task
from profiles.models import Notification, Profile

broker = get_broker()
broker.add_middleware(PeriodiqMiddleware(skip_delay=30))


@actor(periodic=cron("0 6 * * *"))
def tasks_in_default() -> None:
    default = Project.objects.get(name='default')
    for prof in Profile.objects.all():
        tasks = Task.objects.filter(project=default)

        if tasks:
            message = f'You have {tasks.count()} tasks in default project!'
            Notification.objects.update_or_create(
                profile=prof, kind='default', read=False, defaults={'text': message, 'link': '/prod/defaults'}
            )
