import pendulum
import pytest

from factories.productivity import GmailFactory
from factories.user import AdminUser
from productivity import views


@pytest.mark.django_db
class TestGmails:
    """Tests for the views and models of `productivity.models.Gmail`."""
    @staticmethod
    def test_read_mails_view(rf):
        """Tests the rendering of emails view."""
        request = rf.get("/productivity/emails/")
        request.user = AdminUser()
        response = views.read_mails(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_gmail_model_creation():
        """Validates proper creation of gmail model."""
        g = GmailFactory()

        assert g
        assert g.id is not None
        assert g.created_at.timestamp() == pytest.approx(pendulum.now(tz='UTC').timestamp())
        assert g.from_address
        assert isinstance(g.done, bool)
        assert g.thread_id
