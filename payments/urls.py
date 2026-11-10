
from django.urls import path

from .views import (
    PaymentListCreateAPIView,
    PaymentSimulationAPIView,
    AdminPaymentListAPIView,
    AdminPaymentRefundAPIView,
)


urlpatterns = [

    path(
        "",
        PaymentListCreateAPIView.as_view(),
        name="payment-list-create"
    ),

    path(
        "<int:pk>/simulate/",
        PaymentSimulationAPIView.as_view(),
        name="payment-simulate"
    ),

    path(
        "admin/",
        AdminPaymentListAPIView.as_view(),
        name="admin-payment-list"
    ),

    path(
        "admin/<int:pk>/refund/",
        AdminPaymentRefundAPIView.as_view(),
        name="admin-payment-refund"
    ),

]
