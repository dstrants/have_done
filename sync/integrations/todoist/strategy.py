from social_core.backends.oauth import BaseOAuth2


class TodoistOAuth2(BaseOAuth2):
    """Todoist OAuth authentication backend"""
    name = 'todoist'
    AUTHORIZATION_URL = 'https://todoist.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://todoist.com/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','

    @staticmethod
    def get_user_details(response) -> dict:
        """Return user details from todoist account"""
        return {'username': response.get('login')}
