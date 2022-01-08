from django.contrib import admin

from .models import Sync, Repository, PullRequest

admin.site.register(Sync)
admin.site.register(Repository)
admin.site.register(PullRequest)
