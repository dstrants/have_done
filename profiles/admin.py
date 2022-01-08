from django.contrib import admin

from profiles.models import Profile, ProfileSetting

admin.site.register(Profile)
admin.site.register(ProfileSetting)
