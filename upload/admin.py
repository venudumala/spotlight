from django.contrib import admin
from .models import DataQualityCheck, DataSource, Project, Upload

admin.site.register(Upload)
admin.site.register(DataQualityCheck)
admin.site.register(Project)
admin.site.register(DataSource)
