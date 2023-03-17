from django.contrib import admin

from .models import DataQualityCheck, DataSource, DataType, Database, Project, QueryLogs, Upload, WorkflowRules, filterSymbol, goldLayerData

admin.site.register(Database)
admin.site.register(Upload)
admin.site.register(DataQualityCheck)
admin.site.register(Project)
admin.site.register(DataSource)
admin.site.register(QueryLogs)
admin.site.register(DataType)
admin.site.register(filterSymbol)
admin.site.register(goldLayerData)
admin.site.register(WorkflowRules)