from typing import Optional

import pendulum
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token
from social_django.models import UserSocialAuth as usa


class Profile(models.Model):
    """Extra data for the user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.user.username

    @property
    def token(self) -> Optional[Token]:
        if token := Token.objects.filter(user=self.user):
            return token.first()
        return None

    def has_usa(self, provider: str) -> Optional[usa]:
        if usas := self.user.social_auth.filter(provider=provider):
            return usas.first()
        return None

    def access_token(self, provider: str) -> Optional[str]:
        if not (usa := self.has_usa(provider=provider)):
            return None

        return usa.extra_data['access_token']

    def refresh_api_token(self) -> Token:
        if self.token:
            self.token.delete()
        token = Token.objects.create(user=self.user)
        return token


class ProfileSetting(models.Model):
    """Application settings strorage."""
    todoist = models.BooleanField(default=False)
    gmail = models.BooleanField(default=False)
    gcalendar = models.BooleanField(default=False)
    gh_pr = models.BooleanField(default=False)
    uptime_robot = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, verbose_name='settings', related_name='settings',
                                   on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Settings for: " + self.profile.user.username


class Notification(models.Model):
    """User Notification Model."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)
    text = models.TextField(max_length=400)
    link = models.URLField(null=True, blank=True)
    kind = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self) -> str:
        return reverse('profiles:notification', args=[str(self.id)])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs) -> None:
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_user_profile_settings(sender, instance, created, **kwargs):
    if created:
        ProfileSetting.objects.create(profile=instance)


@receiver(pre_save, sender=Notification)
def update_timestamp_when_read(sender, instance, **kwargs):
    if instance.id is None:
        return None

    is_read_already = sender.objects.get(id=instance.id).read
    if instance.read and (not is_read_already):
        instance.read_at = pendulum.now()
