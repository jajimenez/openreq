"""Wait for DB command."""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as PsOperationalError


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **kwargs):
        """Run the command logic."""
        self.stdout.write("Waiting for the database...")
        up = False

        while not up:
            try:
                self.check(databases=["default"])
                up = True
            except (OperationalError, PsOperationalError):
                self.stdout.write(
                    "The database is unavailable. Waiting 1 second..."
                )

                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("The database is available."))
