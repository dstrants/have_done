import pendulum
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import serializers as srs
from .models import Category, Project, Task, TaskAddon, TaskAddonProvider


class CategoryViewSet(ModelViewSet):
    """Implements all the endpoints for the Category Model"""
    serializer_class = srs.CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class ProjectViewSet(ModelViewSet):
    """Implements all the endpoints for the Project Model"""
    serializer_class = srs.ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAdminUser]


class TaskViewSet(ModelViewSet):
    """Implements all the endpoints for the Category Model"""
    serializer_class = srs.TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False)
    def today(self, request):
        """Returns tasks done today."""
        today = pendulum.now().start_of('day')
        qset = Task.objects.filter(created_at__gte=today)
        sers = srs.TaskSerializer(qset, many=True)
        return Response(sers.data)


class TaskAddonViewSet(ModelViewSet):
    """Implements all the endpoints for the Addon Model."""
    serializer_class = srs.TaskAddonSerializer
    queryset = TaskAddon.objects.all()
    permission_classes = [IsAdminUser]


class TaskAddonProviderViewSet(ModelViewSet):
    """Implements all the endpoints for the Addon Model."""
    serializer_class = srs.TaskAddonProviderSerializer
    queryset = TaskAddonProvider.objects.all()
    permission_classes = [IsAdminUser]


class JiraWebhook(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request):
        body = request.data
        category = Category.objects.get(name='task')
        project = Project.objects.get(name='dion')
        addon = f"jira:https://dionsa-it.atlassian.net/browse/{body['key']}"
        task = f"{body['fields']['summary']} {addon}"
        Task.objects.create(
            task=task,
            project=project,
            category=category
        )
        return Response({'status': 'done'})
