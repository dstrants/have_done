from rest_framework.serializers import ModelSerializer

from .models import Category, Project, Task, TaskAddon, TaskAddonProvider


class CategorySerializer(ModelSerializer):
    """Serializes the Category Model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'emoji']


class ProjectSerializer(ModelSerializer):
    """Serializes the Project Model"""

    class Meta:
        model = Project
        fields = ['id', 'name', 'color']


class TaskSerializer(ModelSerializer):
    """Serializes Task Model"""

    class Meta:
        model = Task
        fields = ['id', 'task', 'category', 'project', 'created_at']


class TaskAddonSerializer(ModelSerializer):
    """Serializes TaskAddon Model."""

    class Meta:
        model = TaskAddon
        fields = ['task', 'url', 'uid', 'url', 'provider']


class TaskAddonProviderSerializer(ModelSerializer):
    """Serializes TaskAddonProvider Model."""

    class Meta:
        model = TaskAddonProvider
        fields = ["id", "name", "icon", "color", "shortcut", "base_url"]
