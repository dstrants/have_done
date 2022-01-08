from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from sync.models import Repository
from productivity.models import Category, Project
from sync import tasks
from sync.decorators import todoist
from sync.integrations.uptimerobot.client import UptimeRobot as Uptime
from sync.tasks import import_github_repos


@login_required
@todoist(settings_url='/profile/settings')
def todoist_home(request):
    """Todoist wizard.
    It provides an interface to link local projects
    with todoist projects for seamless sync.
    """
    return render(request, "sync/todoist.html", {'sets': tasks.todoist_secondary(request.user.id)})


@login_required
def link_todoist_to_local_project(request, tid, pid):
    """Links todoist projects to local projects.

    Args:
    tid (int): Todoist Project Id
    pid (int): Local Project Id

    If the pid is zero it just unlinks the todoist project
    from the linked project.
    """
    Project.objects.filter(todoist_id=tid).update(todoist_id=None)
    if pid:
        project = Project.active.get(pk=pid)
        # project = get_object_or_404(Project, pk=pid)
        project.todoist_id = tid
        project.save(update_fields=['todoist_id'])
    if request.is_ajax():
        return JsonResponse({'ok': True, 'tid': tid, 'pid': pid})
    return redirect('/sync/todoist/')


@login_required
def link_todoist_to_local_categories(request, tid, cid):
    """Links todoist labels to local categories.

    Args:
    tid (int): Todoist Label Id
    cid (int): Local Category Id

    If the pid is zero it just unlinks the todoist labels
    from the linked project.
    """
    Category.objects.filter(todoist_id=tid).update(todoist_id=None)
    if cid:
        label = get_object_or_404(Category, pk=cid)
        label.todoist_id = tid
        label.save(update_fields=['todoist_id'])
    if request.is_ajax():
        return JsonResponse({'ok': True, 'tid': tid, 'cid': cid})
    return redirect('/sync/todoist/')


@login_required
def manual_todoist_sync(request):
    """Performs a simple manual sync."""
    tasks.todoist_sync_completed_tasks(request.user.id)
    return JsonResponse({'status': 200, 'message': 'Sync finished successfully'})


@login_required
def uptimerobot_status(request):
    """Checks the uptime robot and returns their status"""
    return render(request, "sync/uptime.html", {'monitors': Uptime().get_monitors()})


@login_required
def github_repos(request):
    """Lists github repos for the request.user."""
    if not cache.get(f"github_repo_sync_user_{request.user.id}"):
        import_github_repos(uid=request.user.id)
    repo_list = Repository.objects.all()
    return render(request, "sync/github.html", {'repos': repo_list})


@login_required
def get_repo_list(request):
    """Renders the partial for the repos list."""
    repo_list = Repository.objects.all()
    return render(request, "sync/_repo_list.html", {'repos': repo_list})


@require_POST
@login_required
def watch_togggle_repo(_, org: str, repo: str):
    """Toggles the watch/unwatch attribute for the given repo."""
    name = f"{org}/{repo}"
    repository = get_object_or_404(Repository, name=name)
    repository.watch = not repository.watch
    repository.save(update_fields=['watch'])
    message = f"Syn is turned {'on' if repository.watch else 'off'} for {name}"
    return JsonResponse({'repo': repo, 'message': message, 'watch': repository.watch})
