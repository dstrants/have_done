import pendulum
import pytest

from factories.logs import BackupFactory


@pytest.mark.django_db
class TestLogsModels:
    @staticmethod
    def test_backup_str():
        """Tests the creation of new backup entries"""
        today = pendulum.now().to_date_string()
        b = BackupFactory()
        assert b.id is not None
        assert str(b.created_at.date()) == today
        assert b.__str__() == f"{b.app}_{b.server}_{today}"
