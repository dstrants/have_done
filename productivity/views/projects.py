from typing import Union

from faker import Faker

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import (HttpResponseBadRequest, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from productivity.models import Project


class ProjectsView(LoginRequiredMixin, TemplateView):
    """Renders the container view for the projects list."""

    template_name = "productivity/projects/list.html"


class ListProjectView(LoginRequiredMixin, ListView):
    """Renders the <li> element for all active projects."""

    model = Project
    queryset = Project.objects.exclude(is_active=False).order_by('name')
    template_name = "productivity/projects/_projects.html"
    context_object_name = "projects"


@login_required
def delete_project(request, pro: int):
    """Deletes an existing project."""
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    try:
        project = Project.objects.get(id=pro)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    else:
        project.delete()
    return JsonResponse({'result': True, 'message': 'Task deleted'})


@login_required
def project_update_view(request, pro: int):
    """Fast update template for the project model."""
    project = get_object_or_404(Project, id=pro)

    return render(request, "productivity/projects/_edit.html", {'project': project})


@login_required
def project_fast_update(request, pro: int, field: str, val: Union[int, str]):
    """Updates a task based on url fields."""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid http method")
    try:
        p = Project.objects.get(pk=pro)
        setattr(p, field, val)
        p.save(update_fields=[field])
    except Exception as e:
        result = {'result': False, 'message': str(e)}
    else:
        result = {'result': True, 'message': f'{field} successfully changed for #{p.name}'}
    return JsonResponse(result)


@login_required
def generate_new_project(request):
    """Generates a placeholder category. This can be immediately editted in the list view."""
    fake = Faker()
    Faker.seed(0)
    Project.objects.create(
        name=fake.domain_word(),
        color=fake.hex_color()
    )
    return JsonResponse({'result': True})
