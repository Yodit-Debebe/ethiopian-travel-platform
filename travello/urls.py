
from django.urls import path

from djapro import settings

from .import views



urlpatterns = [
    path('', views.welcome_page, name='welcome'),  # default route
    path('home/', views.home, name='home'),         # home page
    path('payment/<int:id>/', views.payment, name='payment'),
    path('contact/', views.contact, name='contact'),
    

]

