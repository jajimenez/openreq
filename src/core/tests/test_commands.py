from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase

from psycopg2 import OperationalError as PsOperationalError

from core.models import Incident, ClassificationModel


@patch("core.management.commands.wait_for_db.Command.check")
class NonDbCommandTests(SimpleTestCase):
    """Test the Django commands that don't use the database."""

    def test_wait_for_db_ready(self, patched_check: MagicMock):
        """Test the Wait for DB command when the database is ready.

        :param patched_check: `check` function mock.
        :type patched_check: MagicMock
        """
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(
        self, patched_sleep: MagicMock, patched_check: MagicMock
    ):
        """Test the Wait for DB command when an OperationalError error is
        raised.

        :param patched_sleep: `sleep` function mock.
        :type patched_sleep: MagicMock
        :param patched_check: `check` function mock.
        :type patched_check: MagicMock
        """
        patched_check.side_effect = \
            ([PsOperationalError] * 2) + ([OperationalError] * 3) + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])


class DbCommandTests(TestCase):
    """Test the Django commands that use the database."""

    def test_train_classification_model(self):
        """Test the Train Classification Model command."""
        self.assertEqual(ClassificationModel.objects.count(), 0)

        # Create test users
        user_model = get_user_model()
        users = []

        for u in ["user1", "user2", "user3"]:
            users.append(user_model.objects.create_user(username=u))

        # Create test incidents
        incidents = [
            {
                "opened_by": users[0],
                "subject": "The main process failed"
            },
            {
                "opened_by": users[0],
                "subject": "A function has a bug"
            },
            {
                "opened_by": users[1],
                "subject": "A class must be reviewed as it might contain a bug"
            },
            {
                "opened_by": users[1],
                "subject": "The new release has to be deployed in Production"
            },
            {
                "opened_by": users[1],
                "subject": "We found a bug in the code"
            },
            {
                "opened_by": users[2],
                "subject": "The database doesn't work"
            }
        ]

        for i in incidents:
            Incident(opened_by=i["opened_by"], subject=i["subject"]).save()

        call_command("train_classification_model")
        self.assertEqual(ClassificationModel.objects.count(), 1)
