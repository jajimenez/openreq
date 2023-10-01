"""Wait for DB command."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **kwargs):
        """Run the command logic."""
        pass
