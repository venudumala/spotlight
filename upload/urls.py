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
    path('projectwithds/',views.projectDataSourceData.as_view(),name='projectDataSourceViewSet'),
    path('dataSource/',views.DataSourceView.as_view(),name='DataSourceSerializer')
]