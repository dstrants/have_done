from django.urls import path

from logs import views

app_name = 'logs'

urlpatterns = [
    path('api/pr', views.Changelog.as_view()),
    path('api/', views.BackUpList.as_view()),
    path('prs/', views.pr_list, name='prs'),
    path('', views.BackUpListView.as_view(), name='backups')
]
