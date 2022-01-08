from django.urls import path

from sync import views
from sync import api

app_name = 'sync'
urlpatterns = [
     path('todoist/', views.todoist_home, name='todoist'),
     path('todoist/link/<int:tid>/project/<int:pid>', views.link_todoist_to_local_project,
          name="todoist-link-project"),
     path('todoist/link/<int:tid>/label/<int:cid>', views.link_todoist_to_local_categories,
          name="todoist-link-category"),
     path('todoist/sync/tasks', views.manual_todoist_sync, name='todoist-sync'),
     path("todoist/webhook", api.TodoistWebhook.as_view(), name="todoist_webhook"),
     path('uptimerobot/monitors', views.uptimerobot_status, name='uptimerobot'),
     path("github/", views.github_repos, name='github'),
     path("github/list", views.get_repo_list, name='github_list'),
     path("github/watch/<str:org>/<str:repo>", views.watch_togggle_repo, name='watch-repo')
]
