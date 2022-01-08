from poetry.factory import Factory
from poetry.utils._compat import Path

from django import template

from productivity.models import Gmail

register = template.Library()


@register.simple_tag
def load_mail():
    """Returns the mail count"""
    return Gmail.objects.filter(done=False).count()


@register.simple_tag
def version():
    p = Factory().create_poetry(Path.cwd())
    return p.package.pretty_version
