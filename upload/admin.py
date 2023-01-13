from django.contrib import admin
from .models import DataQualityCheck, Project, Upload

admin.site.register(Upload)
admin.site.register(DataQualityCheck)
admin.site.register(Project)
