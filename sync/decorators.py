from functools import wraps
from typing import Callable, Optional

from django.contrib.auth.decorators import user_passes_test


def todoist(function=None, settings_url=None):
    """
    Decorator for views that check that the user has enabled the todoist integration,
    redirecting to the settings page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.profile.settings.todoist,
        login_url=settings_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def token(func: Callable):
    """
    Checks whether instance(self) has a key attribute and returns None
    if it does not.

    It is used to verify the existance of api tokens.
    """
    @wraps(func)
    def check_key(instance: Optional[Callable], *args, **kwargs):
        if instance.key:
            return func(instance)
        return None
    return check_key
