from django.urls import path,include
from . import views
from rest_framework import routers

router=routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('database/',views.databaseView.as_view(),name='databaseView'),
    path('uploaded_list/',views.uploadView.as_view(),name='uploaded_list'),
    path('uploaded_list/<int:pk>',views.UploadLayerView.as_view()),
    path('dataQualityCheck/',views.dataQualityCheck.as_view(),name='dataQualityCheck'),
    path('getSchemaStructure/',views.getSchemaStructure.as_view(),name='getSchemaStructure'),
    path('getSchemaData/',views.getSchemaData.as_view(),name='getSchemaData'),
    path('project/',views.projectView.as_view(),name='projectView'),
    path('silvergoldtransform/',views.silverGoldTransformView.as_view(),name='silvergoldtansform'),
    path('bronzesilvertransform/',views.bronzeSilverTransform.as_view(),name='bronzeSilverTransform'),
    path('getSilverTable/',views.getSilverTable.as_view(),name='getSilverTable'),
    path('getSilverSchemaStructure/',views.getSilverSchemaStructure.as_view(),name='getSilverSchemaStructure'),
    path('getBronzeTable/',views.getBronzeTable.as_view(),name='getBronzeTable'),
    path('getBronzeSchemaStructure/',views.getBronzeSchemaStructure.as_view(),name='getBronzeSchemaStructure'),
    path('projectwithids/',views.projectDataSourceData.as_view(),name='projectDataSourceViewSet'),
    path('getSilverTableData/<str:table_name>',views.getSilverTableData.as_view()),
    path('getBronzeTableData/<str:table_name>',views.getBronzeTableData.as_view()),
    path('QueryLogs/',views.QueryLogsView.as_view(),name='QueryLogs'),
    path('dataTypeView/',views.dataTypeView.as_view(),name='dataTypeView'),
    path('alterTableSilver/',views.alterTableSilver.as_view(),name='alterTableSilver'),
    path('checkColumnSilverTable/',views.checkColumnSilverTable.as_view(),name='checkColumnSilverTable'),
    path('dataSource/<int:project_id>/<str:data_source>',views.DataSourceView.as_view())
]