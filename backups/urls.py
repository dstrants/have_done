from django.contrib import admin
from django.urls import path, include
from productivity.views import home
from rest_framework.routers import DefaultRouter
from productivity import api


router = DefaultRouter()
router.register('categories', api.CategoryViewSet)
router.register('projects', api.ProjectViewSet)
router.register('tasks', api.TaskViewSet)
router.register('addons', api.TaskAddonViewSet)
router.register('addonproviders', api.TaskAddonProviderViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('backups/', include('logs.urls')),
    path('prod/', include('productivity.urls')),
    path('profile/', include('profiles.urls')),
    path('sync/', include('sync.urls')),
    path('api/', include(router.urls)),
    path('api/jira', api.JiraWebhook.as_view())
]
