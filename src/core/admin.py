from django.contrib import admin

from core.models import Category, Incident


# Register models
admin.site.register(Category)
admin.site.register(Incident)
