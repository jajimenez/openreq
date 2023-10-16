from django.contrib import admin

from core.models import Tag, Incident


# Register models
admin.site.register(Tag)
admin.site.register(Incident)
