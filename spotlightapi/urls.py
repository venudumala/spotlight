from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('upload.urls')),
    path('account/',include('user_app.api.urls')),
    
]
