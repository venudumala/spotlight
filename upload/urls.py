from django.urls import path,include
from . import views
from rest_framework import routers

router=routers.DefaultRouter()
# router.register('uploads',views.UploadView)
# router.register('layer',views.UploadLayerView)

urlpatterns = [
    path('',include(router.urls)),
    path('uploaded_list/',views.uploadView.as_view(),name='uploaded_list'),
    path('uploaded_list/<int:pk>',views.UploadLayerView.as_view(),name='get_uploaded_list_id')
]