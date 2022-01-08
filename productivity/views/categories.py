from typing import Union

from faker import Faker

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from productivity.models import Category


class CategoriesView(LoginRequiredMixin, TemplateView):
    """Static container view to list the categories."""

    template_name = "productivity/categories/list.html"


class ListCategoriesView(LoginRequiredMixin, ListView):
    """Renders the Category <li> element for each category."""

    model = Category
    queryset = Category.objects.all()
    template_name = "productivity/categories/_category.html"
    context_object_name = "categories"


@login_required
def category_update_view(request, cat: int, field: str):
    """Fast update for the category fields."""
    category = get_object_or_404(Category, id=cat)

    return render(request, "productivity/categories/_edit.html", {'cat': category, 'field': field})


@login_required
def delete_category(request, cat: int):
    """Deletes an existing category."""
    if not request.method == 'POST':
        return HttpResponseBadRequest()

    category = get_object_or_404(Category, id=cat)
    category.delete()

    return JsonResponse({'result': True, 'message': 'Task deleted'})


@login_required
def category_fast_update(request, cat: int, field: str, val: Union[int, str]):
    """Updates a task based on url fields."""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid http method")
    try:
        category = Category.objects.get(pk=cat)
        setattr(category, field, val)
        category.save(update_fields=[field])
    except Exception as e:
        result = {'result': False, 'message': str(e)}
    else:
        result = {'result': True, 'message': f'{field} successfully changed for {category.name}'}
    return JsonResponse(result)


@login_required
def generate_new_category(request):
    """Generates a placeholder category. This can be immediately editted in the list view."""
    fake = Faker()
    Faker.seed(0)
    Category.objects.create(name=fake.domain_word(), emoji="🍀")
    return JsonResponse({'result': True})
