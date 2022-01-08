import pendulum
import pytest

from factories.productivity import ProjectFactory, TaskFactory
from factories.profiles import NotificationFactory, ProfileFactory
from factories.user import AdminUser
from profiles.models import Notification
from profiles.tasks import tasks_in_default
from profiles.templatetags.profile_extras import user_notifications
from profiles.views import visit_notification


@pytest.mark.django_db
class TestNotification:
    """Tests regarding the `profile.models.Notification` model."""
    @staticmethod
    def test_notification_model_creation(rf):
        """Tests that the `Notification` model is properly created."""
        notif = NotificationFactory()

        assert notif
        assert notif.id is not None
        assert not notif.read
        assert pytest.approx(pendulum.now().timestamp(), notif.created_at.timestamp)
        assert notif.read_at is None

    @staticmethod
    def test_auto_read_time_field_update() -> None:
        """Checks that the `read_at` field is automatically updated."""
        notif = NotificationFactory()

        assert notif

        assert not notif.read

        notif.read = True
        notif.save()

        notif.refresh_from_db()

        assert notif.read
        assert notif.read_at
        assert pytest.approx(pendulum.now().timestamp(), notif.read_at.timestamp)

    @staticmethod
    def test_visit_notification_view(rf):
        """Tests if visiting the notification marks the notification as read."""
        notif = NotificationFactory()

        assert not notif.read

        request = rf.get(notif.get_absolute_url())
        request.user = AdminUser()
        response = visit_notification(request, id=notif.id)

        assert response
        assert response.status_code == 302
        assert response['Location'] == notif.link

        notif.refresh_from_db()

        assert notif.read

    @staticmethod
    def test_notification_badge_template_tag():
        """Tests that only unread notification as show on the frontend."""
        prof = ProfileFactory()
        for i in range(10):
            NotificationFactory(read=bool(i % 2), profile=prof)

        notifications = user_notifications(user=prof.user)

        assert notifications
        assert notifications.count() == 5
        assert not any((n.read for n in notifications))

    @staticmethod
    def test_the_defaults_notification_generation_task():
        pro = ProjectFactory(name='default')
        ProfileFactory()

        for _ in range(10):
            TaskFactory(project=pro)

        tasks_in_default()

        notif = Notification.objects.get(kind='default', read=False)

        assert notif
        assert notif.text == 'You have 10 tasks in default project!'
