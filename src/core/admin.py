from django.contrib import admin

from core.models import Category, Incident, ClassificationModel


# Register models
admin.site.register(Category)
admin.site.register(Incident)
admin.site.register(ClassificationModel)
