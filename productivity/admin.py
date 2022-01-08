from django.contrib import admin

from .models import Category, Project, Task, TaskAddon, TaskAddonProvider

admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(TaskAddon)
admin.site.register(TaskAddonProvider)
