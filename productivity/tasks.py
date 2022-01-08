import pendulum
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from dramatiq import actor, get_broker
from periodiq import PeriodiqMiddleware, cron
from slack_sdk import WebClient

from productivity.helpers import generate_week_stats
from productivity.models import Task
from sync.integrations.slack.task_block import TaskBlock,\
    MESSAGE_BLOCK as msg_block, DAILY_TASK_REPORT_TEMPLATE


broker = get_broker()
broker.add_middleware(PeriodiqMiddleware(skip_delay=30))


@actor(periodic=cron("30 18 * * 1-5"))
def no_task_mail():
    """Sends an email reminder when no tasks are recorded on a work day"""
    today = pendulum.now().start_of('day')
    client = WebClient(token=settings.SLACK_API_TOKEN)
    if not Task.objects.filter(created_at__gte=today).exists():
        client.chat_postMessage(channel="#tasks", blocks=msg_block)


@actor(periodic=cron('0 8 * * 7'))
def weekly_report() -> None:
    week_no = pendulum.now().week_of_year
    stats = generate_week_stats(week_no=week_no)
    text_body = render_to_string('emails/productivity/weekly.txt', stats)
    html_body = render_to_string('emails/productivity/weekly.html', {'stats': stats})
    msg = EmailMultiAlternatives(
        subject='Backups: Weekly Report',
        from_email='noreply@notify.strdi.me',
        to=['dstrants@gmail.com'],
        body=text_body
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


@actor(periodic=cron("25 10 * * 2-5"))
def daily_stand_up_report() -> None:
    """Sends daily report on weekdays."""
    yesterday = pendulum.yesterday().start_of('day')
    client = WebClient(token=settings.SLACK_API_TOKEN)
    if tasks := Task.objects.filter(created_at__gte=yesterday):
        tpl = DAILY_TASK_REPORT_TEMPLATE + [TaskBlock(task).task_block() for task in tasks]
        client.chat_postMessage(channel="#tasks", blocks=tpl)
