from typing import List, Optional

import pendulum

from productivity.models import Task

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday']


def unique_task_field(tasks, field: str = 'project') -> set:
    """Returns an array of unique projects included in qset"""
    return {getattr(t, field) for t in tasks}


def generate_week_stats(week_no: int) -> Optional[dict]:
    """Generate a dict with current week stats"""
    tasks = Task.objects.filter(created_at__week=week_no, created_at__year=pendulum.now().year)
    days = {}
    for n in range(1, 8):
        days[DAYS[n-1]] = tasks.filter(created_at__week_day=n)
    if tasks:
        return {
            'days': days,
            'task_count': tasks.count(),
            'task_count_ratio': round(tasks.count()*100 / 25, 2),
            'max_day': weekday_with_most_tasks(tasks),
            'counts_array': task_count_per_day(tasks),
            'max_category': category_with_most_tasks(tasks),
            'counts_cat': tasks_count_per_category(tasks),
            'categories': [c.name for c in unique_task_field(tasks, 'category')],
            'projects': [p.name for p in unique_task_field(tasks, 'project')],
            'max_project': project_with_most_tasks(tasks),
            'counts_pro': tasks_count_per_project(tasks)
        }
    return None


def weekday_with_most_tasks(tasks) -> tuple:
    """Finds the most productive day this week"""
    counts = task_count_per_day(tasks)
    mx = max(counts) or 0
    return DAYS[counts.index(mx)], mx


def task_count_per_day(tasks) -> List[int]:
    """Counts the total tasks per day this week"""
    return [tasks.filter(created_at__week_day=i).count() for i in range(1, 8)]


def tasks_count_per_project(tasks) -> List[int]:
    """Count tasks per project"""
    return [tasks.filter(project=project).count() for project in unique_task_field(tasks, 'project')]


def project_with_most_tasks(tasks) -> tuple:
    """Returns the project with most tasks this week"""
    projects = list(unique_task_field(tasks, 'project'))
    mx = max(tasks_count_per_project(tasks))
    return projects[tasks_count_per_project(tasks).index(mx)], mx


def tasks_count_per_category(tasks) -> List[int]:
    """Count tasks per category"""
    return [tasks.filter(category=c).count() for c in unique_task_field(tasks, 'category')]


def category_with_most_tasks(tasks) -> tuple:
    """Returns the category with most tasks this week"""
    categories = list(unique_task_field(tasks, 'category'))
    mx = max(tasks_count_per_category(tasks))
    return categories[tasks_count_per_category(tasks).index(mx)], mx
