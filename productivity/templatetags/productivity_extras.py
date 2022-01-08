from typing import Any, Union

import pendulum
from django import template

from productivity.models import Category, Project

register = template.Library()


@register.filter
def day_of_date(day: str) -> str:
    """Returns the day of the month for the given date"""
    return pendulum.parse(day).format("DD")


@register.filter
def get_attr(model:  Union[Category, Project], field: str) -> Any:
    """Template version of built-in method getattr"""
    return getattr(model, field)
