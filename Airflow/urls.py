from django.urls import path,include
from . import views

urlpatterns = [
    path('sourcetest/',views.sourceTestMssql.as_view(), name='sourcetest'),
]