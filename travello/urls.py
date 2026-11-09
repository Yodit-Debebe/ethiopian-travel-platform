
from django.urls import path

from .import views



urlpatterns = [
    path('', views.welcome_page, name='welcome'),  # default route
    path('home/', views.home, name='home'),         # home page
    path('payment/<int:id>/', views.payment, name='payment'),
    path('contact/', views.contact, name='contact'),

    path(
        'api/destinations/',
        views.DestinationListAPIView.as_view(),
        name='destination-list-api'
    ),

    path(
    'api/destinations/<int:pk>/',
    views.DestinationDetailAPIView.as_view(),
    name='destination-detail-api'
),
    path(
    'api/destinations/create/',
    views.DestinationCreateAPIView.as_view(),
    name='destination-create-api'
),

]

