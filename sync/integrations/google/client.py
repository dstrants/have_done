from typing import Optional

import pendulum
from django.contrib.auth.models import User
from googleapiclient import discovery

from productivity.models import Gmail
from sync.integrations.google.credentials import Credentials


class GoogleClient:
    """Simple client to perform the interactions with google APIs."""
    def __init__(self, user: User) -> None:
        self.user: User = user

        # User social auths
        self.usas = user.social_auth.filter(provider='google-oauth2')

    def _events(self, params: Optional[dict] = None):
        """Abstract method to consume the event api."""
        params = {} if not params else params
        events = []
        kwargs = {
            'calendarId': 'primary', 'timeMin': pendulum.now().isoformat(),
            'maxResults': 5, 'singleEvents': True, 'orderBy': 'startTime'
        } | params
        for usa in self.usas:
            service = discovery.build('calendar', 'v3', credentials=Credentials(usa))
            event_results = service.events().list(**kwargs).execute()
            events.extend(event_results.get('items', []))
        return events

    def get_emails(self, query: str = '', save: bool = True) -> list[dict]:
        """Method tha retrieves and optionally saves emails to the db."""
        mails = []
        for usa in self.usas:
            service = discovery.build('gmail', 'v1', credentials=Credentials(usa))
            emails = service.users().threads().list(userId=usa.uid, q=query).execute()
            if emails['resultSizeEstimate'] > 0:
                for email in emails['threads']:
                    mail = service.users().threads().get(userId=usa.uid, id=email['id']).execute()
                    payload = mail['messages'][0]['payload']
                    subject = [t['value'] for t in payload['headers'] if t['name'] == 'Subject'][0]
                    fr = [t['value'] for t in payload['headers'] if t['name'] == 'From'][0]
                    mails.append({'thread_id': email['id'], 'subject': subject, 'from_address': fr})
                    if save:
                        Gmail.objects.update_or_create(
                            thread_id=email['id'],
                            defaults={'subject': subject, 'from_address': fr, 'done': False}
                        )
        return mails

    def get_events(self) -> list[dict]:
        """Alias for retrieving the next 5 events."""
        return self._events()

    def todays_events(self) -> list[dict]:
        """Alias for retrieving today's events."""
        params = {'timeMin': pendulum.today().isoformat(), 'timeMax': pendulum.now().isoformat()}
        return self._events(params=params)
