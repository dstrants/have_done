from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView

from productivity.models import TaskAddonProvider


class CreateAddonProviderView(LoginRequiredMixin, CreateView):
    """Create a new addon provider"""

    model = TaskAddonProvider
    fields = ['name', 'icon', 'color', 'shortcut', 'base_url']


class ListAddonProviderView(LoginRequiredMixin, ListView):
    """Lists all available addon providers"""

    model = TaskAddonProvider


class UpdateAddonProviderView(LoginRequiredMixin, UpdateView):
    """Updates one or more of the below field on a dedicated view"""

    model = TaskAddonProvider
    fields = ['name', 'icon', 'color', 'shortcut', 'base_url']
