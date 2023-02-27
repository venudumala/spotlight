from django.urls import path,include
from . import views

urlpatterns = [
    path('sourcetest/',views.sourceTestMssql.as_view(), name='sourcetest'),
    path('getSourceId/',views.getSourceID.as_view(), name='sourceid'),
    path('getConnId/',views.getConnId.as_view(), name='connid'),
    path('getTableList/',views.getTablesList.as_view(), name='tables'),
    path('syncConnection/',views.syncConnection.as_view(), name='SyncConnection'),
    path('syncCsvFile/',views.syncCsvFile.as_view(), name='CSVFile'),
    path('syncAzureBlob/',views.syncAzureBlob.as_view(),name='AzureBlob'),
]