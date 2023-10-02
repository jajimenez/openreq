from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

from psycopg2 import OperationalError as PsOperationalError


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test the Django commands."""

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
