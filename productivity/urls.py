from django.urls import path

from productivity import views

app_name = 'prod'

urlpatterns = [
    path('today/', views.today, name='today'),
    path('week/', views.this_week, name='this_week'),
    path('today/refresh', views.tasks_today, name='refresh'),
    path('category/find', views.find_category, name='find_category'),
    path('category/create', views.create_category, name='create_category'),
    path('defaults/', views.tasks_in_default, name='defaults'),
    path('project/find', views.find_project, name='find_project'),
    path('project/create', views.create_project, name='create_project'),
    path('tasks/create', views.create_task, name='task_create'),
    path('tasks/delete', views.delete_task, name='task_delete'),
    path('tasks/<int:tid>/addon', views.add_new_addon, name='task_addon'),
    path('tasks/project/<str:pro>', views.find_by_project, name='by_project'),
    path('tasks/fu/<int:task>/<str:field>/<int:val>', views.task_fast_update, name='tfu'),
    path('tasks/fu/<int:task>/<str:field>/<str:val>', views.task_fast_update, name='tfu'),
    path('emails/', views.read_mails, name='mails'),
    path('emails/import', views.import_emails, name='import_mails'),
    path('events/import', views.import_events, name='import_events'),
    path('providers/create', views.CreateAddonProviderView.as_view(), name='provider_create'),
    path('providers/', views.ListAddonProviderView.as_view(), name='providers_list'),
    path('providers/update/<int:pk>', views.UpdateAddonProviderView.as_view(), name='providers_update'),
    path('projects/list', views.ProjectFastUpdateListView.as_view(), name='projects_quicklist'),
    path('categories/list', views.CategoryFastUpdateListView.as_view(), name='categories_quicklist'),
    path('task/<int:task>/list', views.task_text_fast_update_view, name='text_quicklist'),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("projects/new", views.generate_new_project, name='generate_project'),
    path("projects/delete/<int:pro>", views.delete_project, name='delete_project'),
    path("projects/partial", views.ListProjectView.as_view(), name="projects_list_partial"),
    path('projects/fu/<int:pro>/<str:field>/<int:val>', views.project_fast_update, name='pfu'),
    path('projects/fu/<int:pro>/<str:field>/<str:val>', views.project_fast_update, name='pfu'),
    path('projects/update/template/<int:pro>', views.project_update_view, name='project_update'),
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path("categories/new", views.generate_new_category, name='generate_category'),
    path("categories/partial", views.ListCategoriesView.as_view(), name="categories_list_partial"),
    path("categories/delete/<int:cat>", views.delete_category, name='delete_category'),
    path('categories/update/template/<int:cat>/<str:field>', views.category_update_view, name='cat_update'),
    path('categories/fu/<int:cat>/<str:field>/<str:val>', views.category_fast_update, name='cfu'),
    ]
