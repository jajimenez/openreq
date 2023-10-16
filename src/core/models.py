"""Core models."""
from django.db.models import Model, ForeignKey, CASCADE, CharField, TextField
from django.conf.global_settings import AUTH_USER_MODEL


# class Tag(Model):
#     """Tag model."""

#     pass


class Incident(Model):
    """Incident model."""

    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    subject = CharField(null=False, blank=False, max_length=200)

    description = TextField(
        null=True, blank=True, default=None, max_length=2000
    )

    def __str__(self):
        """Get the string representation of the instance."""
        max_length = 50

        if len(self.subject) > max_length:
            return self.subject[:max_length - 2] + "..."
        else:
            return self.subject
