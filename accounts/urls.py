from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name='login'),

    path(
    'api/register/',
    views.RegisterAPIView.as_view(),
    name='register-api'
    ),

    path(
    'api/login/',
    views.LoginAPIView.as_view(),
    name='login-api'
    ),

    path(
    'api/logout/',
    views.LogoutAPIView.as_view(),
    name='logout-api'
),

]