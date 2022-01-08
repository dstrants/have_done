from typing import Union

from django.contrib.auth.models import User
from github import Github
from github.Repository import Repository as Repo


def set_changelog_body(repo: Repo) -> str:
    """Updates the CHANGELOG body with the changes mentioned in PRs body"""
    pulls = repo.get_pulls(state='closed', base='master')
    body = ''
    for pr in pulls:
        if pr.merged_at:
            body += '\n## ' + str(pr.merged_at) + '\n' + pr.body + '\n'
    return body


def update_changelog(repo: str, uid: str) -> Union[str, dict]:
    """Updates the changes log file with the incoming changes."""
    user = User.objects.get(social_auth__provider='github', social_auth__uid=uid)
    if not (key := user.profile.access_token('github')):
        return {'status': 404, 'message': 'Github User Not Found'}
    g = Github(key)
    repository = g.get_repo(repo)
    body = set_changelog_body(repository)
    changelog = repository.get_contents("changelog.md")
    repository.update_file(changelog.path, "Updating Changelog", body, changelog.sha)
    return 'Done'
