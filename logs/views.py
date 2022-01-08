"""
API & Regular views of backups
"""
import pendulum
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from logs import helpers
from logs.models import Backup
from logs.serializers import BackUpSerializer
from sync.models import PullRequest
from sync.tasks import import_user_prs


def bck_status() -> dict:
    sts = {}
    one_month_ago = pendulum.now().subtract(months=1).start_of('day')
    ts = pendulum.now(tz=settings.TIME_ZONE).start_of('day')
    apps = Backup.objects.filter(created_at__gte=one_month_ago)\
                         .values_list('app', flat=True).order_by().distinct()
    for app in apps:
        sts[app] = Backup.objects.filter(app=app, created_at__gte=ts).exists()
    return sts


class BackUpList(APIView):
    """
    Creates new backups
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, format=None):
        serializer = BackUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BackUpListView(LoginRequiredMixin, ListView):
    model = Backup
    paginate_by = 10


class Changelog(APIView):
    """
    Creates new Changelog
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, format=None):
        # TODO: Improve the security verification
        try:
            sha_name = request.headers['X-Hub-Signature'].split('=')[0]
        except (KeyError, AttributeError):
            sha_name = 0
        if sha_name != 'sha1':
            return Response({'status': 'Not Github'}, status=status.HTTP_401_UNAUTHORIZED)
        if (request.data['ref'] == "refs/heads/master" and
                'changelog.md' not in request.data['head_commit']['modified'] and
                request.data['head_commit']['message'] != "Updating Changelog"):
            uid = request.data['sender']['id']
            helpers.update_changelog(request.data['repository']['full_name'], uid)
            return Response({'status': 'done'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Ignored', 'reason': 'Not master commit'},
                            status=status.HTTP_208_ALREADY_REPORTED)


@login_required
def pr_list(request):
    """Returns an html list of 10 latest prs."""
    # Check if user has signed in with github
    if not request.user.profile.has_usa('github'):
        return render(request, "logs/github_auth.html")

    # Force sync if triggered through the UI.
    if request.GET.get('force_sync'):
        import_user_prs(request.user.id)

    prs = PullRequest.objects.exclude(status='closed').order_by('-created_at')[:10]
    return render(request, "logs/prs.html", {'prs': prs})
