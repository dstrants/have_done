import logging
from datetime import datetime
from typing import List, Optional

import pendulum
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from dramatiq import actor, get_broker
from github import Github
from github.PullRequest import PullRequest as Pr
from periodiq import PeriodiqMiddleware, cron

from logs.models import Backup
from sync.models import Repository, PullRequest
from productivity.models import Category, Gmail, Project, Task
from sync.integrations.google.client import GoogleClient as Google
from sync.integrations.todoist.client import TodoistClient

broker = get_broker()
broker.add_middleware(PeriodiqMiddleware(skip_delay=30))

logger = logging.getLogger(__name__)

# TODOIST TASKS


@actor
def todoist_secondary(uid: int) -> dict:
    """Forms a dict of projects and categories fetched for todoist."""
    return {
        'projects': todoist_projects(uid),
        'categories': todoist_categories(uid)
    }


@actor
def todoist_projects(uid: int) -> Optional[List[tuple]]:
    """Matches todoist projects with local ones."""
    if not (user := User.objects.get(id=uid)):
        return None
    t = TodoistClient(user)
    projects = t.projects()
    matches = []
    for pro in projects:
        if match := Project.objects.filter(todoist_id=pro.id):
            matches.append((pro, match.first()))
        elif match := Project.objects.filter(name__icontains=pro.name):
            matches.append((pro, match.first()))
    return matches


@actor
def todoist_categories(uid: int) -> Optional[List[tuple]]:
    """Matches todoist labels with local categories."""
    if not (user := User.objects.get(id=uid)):
        return None
    t = TodoistClient(user)
    matches = []
    for label in t.labels():
        if match := Category.objects.filter(todoist_id=label.id):
            matches.append((label, match.first()))
        elif match := Category.objects.filter(name__icontains=label.name):
            matches.append((label, match.first()))
    return matches


@actor
def todoist_sync_completed_tasks(uid: int) -> None:
    """Syncs completed tasks that have not been delivered with a webhook to the database."""
    if not (user := User.objects.get(id=uid)):
        return None
    t = TodoistClient(user)
    tasks = t.completed_tasks()
    existing_tasks = set(Task.objects.filter(todoist_id__isnull=False).values_list('todoist_id', flat=True))
    tasks_to_create = filter(lambda t: t.id not in existing_tasks, tasks)
    for task in tasks_to_create:
        try:
            task.save_to_mongo()
            task.save()
        except Exception:
            pass
    return None


@actor(periodic=cron('0 */8 * * *'))
def sync_todoist() -> None:
    """Syncs todoists tasks for all users."""
    for user in User.objects.all():
        if user.profile.settings.todoist:
            todoist_sync_completed_tasks.send(user.id)


# GOOGLE TASKS


@actor
def check_for_read(emails: list) -> None:
    """Checks for archived mails."""
    threads = [mail['id'] for mail in emails if 'id' in mail]
    Gmail.objects.filter(done=False).exclude(thread_id__in=threads).update(done=True)


@actor
def import_user_emails(user_id: int) -> None:
    """Imports new thread to the db for the given user."""
    user = User.objects.get(pk=user_id)
    g = Google(user=user)

    if mails := g.get_emails(query='label: Pending is:inbox'):
        return check_for_read.send(mails)

    Gmail.objects.all().update(done=True)


@actor
def import_user_events(user_id: int) -> None:
    """Import google calendar event for given user."""
    user = User.objects.get(pk=user_id)
    g = Google(user=user)

    events = g.get_events()

    cache.set(f"{user.username}_events", events, timeout=3600*6)


@actor(periodic=cron('0 * * * *'))
def fetch_emails() -> None:
    """Loops through users and syncs their mails."""
    for user in User.objects.all():
        import_user_emails.send(user_id=user.id)
        import_user_events.send(user_id=user.id)


@actor
def events_to_tasks(user_id: int) -> None:
    """Imports todays events as tasks."""
    user = User.objects.get(pk=user_id)
    g = Google(user=user)
    cat = Category.objects.get(name='meeting')
    pro = Project.objects.get(name='default')

    events = g.todays_events()

    for meeting in events:
        tsk = f"{meeting['summary']} gcal:{meeting['htmlLink']}"
        Task.objects.create(
            category=cat,
            task=tsk,
            project=pro
        )


@actor
def gmails_to_tasks(user_id: int) -> None:
    """Sync sent emails to tasks."""
    user = User.objects.get(pk=user_id)
    g = Google(user=user)
    cat = Category.objects.get(name='mail')
    pro = Project.objects.get(name='default')

    emails = g.get_emails('in:sent newer_than:20h', save=False)
    for email in emails:
        tsk = f"{email['subject']} gmail:{email['thread_id']}"
        Task.objects.create(
            category=cat,
            task=tsk,
            project=pro
        )


@actor(periodic=cron('0 20 * * *'))
def all_google_to_tasks() -> None:
    """Trigger event import for all users."""
    for user in User.objects.all():
        events_to_tasks.send(user.id)
        gmails_to_tasks.send(user.id)


@actor(periodic=cron('0 0 * * *'))
def daily_backups() -> None:
    """Performs daily backups of database and media."""
    call_command('dbbackup', '--clean', '--compress')
    call_command('mediabackup', '--clean', '--compress')
    Backup.objects.create(
        app='backups', total_size=None, total_files=2,
        server='backups.p.strdi.me', status=True,
        log='https://backups.p.strdi.me'
    )


@actor
def import_github_repos(uid: int) -> None:
    """Imports github repositories into local model."""
    user = User.objects.get(pk=uid)

    logger.info("Importing repositories for user: %s", user.username)

    if not (key := user.profile.access_token('github')):
        logger.error("Not github credentials found for user %s", user.username)
        return None

    g = Github(key)
    repos = g.get_user().get_repos()
    repositories = [Repository(name=repo.full_name, private=repo.private) for repo in repos]
    Repository.objects.bulk_create(repositories, ignore_conflicts=True)
    cache.set(f"github_repo_sync_user_{user.id}", True, timeout=3600)
    logger.info("Github repo sync finished for %s", user.username)
    repo_names = {repo.full_name for repo in repos}

    deleted, _ = Repository.objects.exclude(name__in=repo_names).delete()
    if deleted:
        logger.info("Clean Up: Deleted %s old repositories", deleted)
    else:
        logger.info("Clean Up: No old repos found")

    return None


def to_local(dt: Optional[datetime]) -> Optional[datetime]:
    """Adds the missing timezone annotation to datetime fields coming for the gh API."""
    if dt:
        return pendulum.parser.parse(str(dt), timezone='UTC')
    return None


def pr_kwargs(pr: Pr) -> dict:
    """Prepares the parameters dict for the PullRequest model from the API data"""
    return {'html_url': pr.html_url, 'status': pr.state, 'opened_by': pr.user.login,
            'created_at': to_local(pr.created_at), 'user_url': pr.user.avatar_url,
            'updated_at': to_local(pr.updated_at), 'title': pr.title, 'closed_at': to_local(pr.closed_at),
            'merged_at': to_local(pr.merged_at), 'repo_name': pr.head.repo.name}


@actor
def import_user_prs(uid: int) -> None:
    """Import today's pr into tasks for the given user."""
    user = User.objects.get(pk=uid)
    logger.info("Starting github PRs sync for user %s", user.username)

    # Check if user has credentials
    if not (key := user.profile.access_token('github')):
        logger.error("Not github credentials found for user %s", user.username)
        return None

    # Initiates gh client
    g = Github(key)
    gh_user_name = g.get_user().login

    # Iterate user repos that are watched.
    for local_repo in Repository.objects.filter(watch=True):
        logger.info("Checking repo: %s", local_repo.name)
        repo = g.get_repo(local_repo.name)
        pulls = [pr for state in ('open', 'closed') for pr in repo.get_pulls(state=state)]
        # Iterate repo pull requests that the user is author of.
        for pr in filter(lambda pr: pr.user.name != gh_user_name, pulls):
            logger.info("Repo -> %s Found PR: #%s status: %s", repo.name, pr.number, pr.state)
            PullRequest.objects.update_or_create(
                number=pr.number,
                repo_full_name=repo.full_name,
                defaults=pr_kwargs(pr)
            )

    logger.info("Github PRs import finished for user %s", user.username)
    return None


@actor(periodic=cron("0/5 * * * *"))
def import_github_pull_request() -> None:
    """Triggers a github pr import for each user."""
    for user in User.objects.filter(social_auth__provider="github"):
        import_user_prs.send(user.id)
