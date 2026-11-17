from django.urls import path

from . import views


urlpatterns = [
    path(
        'register/',
        views.RegisterAPIView.as_view(),
        name='register-api'
    ),
    path(
        'login/',
        views.LoginAPIView.as_view(),
        name='login-api'
    ),
    path(
        'logout/',
        views.LogoutAPIView.as_view(),
        name='logout-api'
    ),
    path(
        'profile/',
        views.UserProfileAPIView.as_view(),
        name='profile-api'
    ),
]
