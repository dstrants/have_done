from django import template
from django.db.models import QuerySet

register = template.Library()


@register.simple_tag
def has_usa(user, provider: str):
    return user.profile.has_usa(provider=provider)


@register.simple_tag
def user_notifications(user) -> QuerySet:
    return user.profile.notifications.filter(read=False)
