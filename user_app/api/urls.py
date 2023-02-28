from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import LoginView, logout_view, registration_view
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('login/', LoginView.as_view(),name='login'),
    path('register/', registration_view,name='register'),
    path('logout/', logout_view,name='logout'),
]