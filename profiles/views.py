from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView

from profiles.models import Notification, Profile, ProfileSetting


class SettingsView(LoginRequiredMixin, UpdateView):
    """Changes the settings of the user"""
    model = ProfileSetting
    fields = ['todoist', 'gmail', 'gcalendar', 'gh_pr', 'uptime_robot']
    template_name_suffix = '_edit'

    def get_object(self):
        return self.request.user.profile.settings

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return '/profile/settings/'


class AvatarUpdateview(LoginRequiredMixin, UpdateView):
    """Updates Profile Model."""

    model = Profile
    fields = ['avatar']
    template_name_suffix = '_edit'

    def get_object(self):
        """Retrieves the object that the class will update."""
        return self.request.user.profile

    def get_success_url(self):
        """Redirects the user to the same page after successfully updated avatar."""
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return '/profile/avatar/'


@login_required
def refresh_token(request):
    """Refreshes users api token."""
    token = request.user.profile.refresh_api_token()
    return JsonResponse({'token': token.key})


@login_required
def visit_notification(request, id: int):
    """Redirects to the notification's context."""
    notif = get_object_or_404(Notification, id=id)

    if not notif.read:
        notif.read = True
        notif.save(update_fields=('read',))

    return redirect(notif.link)
