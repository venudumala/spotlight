from django.contrib import admin
from .models import DataQualityCheck, DataSource, Database, Project, QueryLogs, Upload

admin.site.register(Database)
admin.site.register(Upload)
admin.site.register(DataQualityCheck)
admin.site.register(Project)
admin.site.register(DataSource)
admin.site.register(QueryLogs)
