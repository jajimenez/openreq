"""OpenReq - Core - Models."""

from django.db.models import (
    Model, CharField, TextField, BooleanField, ForeignKey, CASCADE, SET_NULL,
    ManyToManyField
)
from django.conf.global_settings import AUTH_USER_MODEL


def _get_summarized_value(value: str, max_length: int = 50) -> str:
    """Get a summarized representation of a string value.

    :param value: Value to represent.
    :type value: str
    :param max_length: Maximum length of the representation.
    :type max_length: int
    :return: Value representation.
    :rtype: str
    """
    if len(value) > max_length:
        return value[:max_length - 2] + "..."
    else:
        return value


class Tag(Model):
    """Tag model."""

    name = CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        """Get the string representation of the instance."""
        return _get_summarized_value(self.name)


class Incident(Model):
    """Incident model."""

    opened_by = ForeignKey(
        AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="opened_incidents"
    )

    subject = CharField(max_length=200)

    description = TextField(
        null=True, blank=True, default=None, max_length=2000
    )

    tags = ManyToManyField("Tag", blank=True)

    assigned_to = ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        default=None,
        on_delete=SET_NULL,
        related_name="assigned_incidents"
    )

    closed = BooleanField(default=False)

    def __str__(self):
        """Get the string representation of the instance."""
        return _get_summarized_value(self.subject)
