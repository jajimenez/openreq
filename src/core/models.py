"""Core models."""
from django.db.models import Model, ForeignKey, CASCADE, TextField
from django.conf.global_settings import AUTH_USER_MODEL


# class Tag(Model):
#     """Tag model."""

#     pass


class Incident(Model):
    """Incident model."""

    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    description = TextField(blank=True, max_length=1000)

    def __str__(self):
        """Get the string representation of the instance."""
        if len(self.description) > 30:
            return self.description[:28] + "..."
        else:
            return self.description
