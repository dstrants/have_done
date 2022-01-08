from typing import Union

import pendulum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import (HttpResponseBadRequest, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import HttpResponse, redirect, render
from django.utils import timezone
from django.views.generic import ListView
from pendulum.parsing.exceptions import ParserError

from sync.tasks import import_user_emails, import_user_events

from productivity import helpers
from productivity.models import (Category, Gmail, Project, Task, TaskAddon,
                                 TaskAddonProvider)

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday']


@login_required
def home(request):
    """Renders the homepage of the app."""
    from logs.views import bck_status
    tasks = Task.objects.filter(created_at__gte=timezone.now().date())[:10]
    return render(request, 'home.html', {'mails': Gmail.objects.filter(done=False),
                                         'status': bck_status(), 'tasks': tasks})


@login_required
def today(request):
    """Renders the tasks of the day"""
    return render(request, "productivity/today.html", {'ctx': 'today'})


@login_required
def this_week(request):
    """Returns the tasks of the current week in calendar format"""
    week_no = request.GET.get('week_no') or pendulum.now().week_of_year
    if not 0 < int(week_no) <= 54:
        return HttpResponseBadRequest("Week number was not valid")
    return render(request, "productivity/week.html", {'week_no': week_no,
                                                      'stats': helpers.generate_week_stats(week_no=week_no)})


@login_required
def tasks_today(request):
    """Returns the list with the tasks of the day"""
    try:
        date = pendulum.parser.parse(request.GET.get('date'))
    except (ParserError, TypeError):
        date = pendulum.now()
    tasks = Task.objects.filter(created_at__range=[date.start_of('day'), date.end_of('day')])
    projects = helpers.unique_task_field(tasks, 'project')
    tod = date.date() == pendulum.now().date()
    return render(request, "productivity/todays_tasks.html", {'tasks': tasks, 'pro': projects,
                                                              'today': tod})


@login_required
def find_category(request):
    """Locates a category based on its name."""
    cat = request.GET.get('cat')
    try:
        cat = Category.objects.get(name__icontains=cat)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return HttpResponse('Not Found')
    else:
        res = serializers.serialize('python', [cat])
        return JsonResponse(res, safe=False)


@login_required
def find_project(request):
    """Locates a project based on its name."""
    pro = request.GET.get('pro')
    try:
        cat = Project.active.get(name__icontains=pro)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return HttpResponse('Not Found')
    else:
        res = serializers.serialize('python', [cat])
        return JsonResponse(res, safe=False)


@login_required
def create_task(request):
    """Async task creation from today's view."""
    if request.method != "POST":
        return HttpResponseBadRequest("Bad request method")

    if not ((cid := request.GET.get('cat_id')) and (pro := request.GET.get('pro'))):
        return HttpResponseBadRequest("Missing category or project parameter.")

    if not (name := request.GET.get('name')):
        return HttpResponseBadRequest("Missing task content.")

    cat = Category.objects.get(id=cid)
    project = Project.objects.get(id=pro)
    Task.objects.create(task=name, category=cat, project=project)
    return redirect('prod:refresh')


@login_required
def delete_task(request):
    """Deletes an existing task."""
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    try:
        pk = request.GET.get('task')
        task = Task.objects.get(id=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    else:
        task.delete()
    return JsonResponse({'result': True, 'message': 'Task deleted'})


@login_required
def find_by_project(request, pro: str):
    """Locats all tasks of a project"""
    try:
        pro = Project.objects.get(name=pro)
    except Project.DoesNotExist:
        return HttpResponseNotFound("Project does not exist")
    tasks = Task.objects.filter(project=pro)
    return render(request, "productivity/todays_tasks.html", {'tasks': tasks, 'pro': []})


@login_required
def tasks_in_default(request):
    """Locates all tasks in default project"""
    if not Project.objects.filter(name='default').exists():
        return redirect("prod:today")
    return render(request, "productivity/today.html", {'ctx': 'defaults'})


@login_required
def create_category(request):
    """Creates new category"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    name = request.GET.get('name')
    emoji = request.GET.get('emoji')
    try:
        Category.objects.create(name=name, emoji=emoji)
    except:
        return HttpResponseBadRequest()
    return JsonResponse({'success': f'Category @{name} created'})


@login_required
def create_project(request):
    """Creates new project"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    name = request.GET.get('name')
    color = request.GET.get('color')
    try:
        Project.objects.create(name=name, color=color)
    except:
        return HttpResponseBadRequest()
    return JsonResponse({'success': f'Project #{name} created'})


@login_required
def read_mails(request):
    """Returns the email table view."""
    return render(request, 'productivity/emails.html', {'mails': Gmail.objects.filter(done=False)})


@login_required
def import_emails(request):
    """Imports mails from Gmail with the label:Pending."""
    import_user_emails.send(request.user.id)
    return JsonResponse({'result': 'Email sync request sent!'})


@login_required
def import_events(request):
    """Importing Events from GCalendar"""
    if request.GET.get('force_sync'):
        import_user_events.send(request.user.id)

    events = cache.get(f"{request.user.username}_events")
    if events:
        events = filter(lambda e: 'start' in e and 'dateTime' in e['start'], events)
        events = list(sorted(events, key=lambda e: pendulum.parse(e['start']['dateTime'])))[:5]
    return render(request, "productivity/_events.html", {'events': events})


@login_required
def add_new_addon(request, tid):
    """Adds new addon to existing task."""
    if request.method == 'POST':
        provider = request.POST.get('pid')
        uid = request.POST.get('uid')
        addon = TaskAddon(task_id=tid, provider_id=provider)
        if uid.startswith('http'):
            addon.url = uid
        else:
            addon.uid = uid
        addon.save()
        return redirect('prod:today')
    providers = TaskAddonProvider.objects.order_by('name')
    return render(request, "productivity/_taskaddon.html", {'providers': providers, 'tid': tid})


@login_required
def task_fast_update(request, task: int, field: str, val: Union[int, str]):
    """Updates a task based on params"""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid http method")
    try:
        t = Task.objects.get(pk=task)
        setattr(t, field, val)
        t.save(update_fields=[field])
    except Exception as e:
        result = {'result': False, 'message': str(e)}
    else:
        result = {'result': True, 'message': f'{field} successfully changed'}
    return JsonResponse(result)


@login_required
def task_text_fast_update_view(request, task: int):
    """Updates the tasks text"""
    t = Task.objects.get(pk=task)
    return render(request, "productivity/_task_edit.html", {'task': t})


class ProjectFastUpdateListView(LoginRequiredMixin, ListView):
    """
    Helping view that lists all projects in a partial.

    This is only used for the task fast update functionality
    """

    model = Project
    template_name = "productivity/_projects_select.html"
    context_object_name = 'projects'
    queryset = Project.active.all()


class CategoryFastUpdateListView(LoginRequiredMixin, ListView):
    """
    Helping view that lists all categories in a partial.

    This is only used for the task fast update functionality
    """

    model = Category
    template_name = "productivity/_categories_select.html"
    context_object_name = 'categories'
