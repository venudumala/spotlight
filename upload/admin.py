from django.contrib import admin
from .models import DataQualityCheck, Upload

admin.site.register(Upload)
admin.site.register(DataQualityCheck)
