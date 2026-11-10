
from django.urls import path
from .views import AdminBookingListAPIView, AdminBookingManageAPIView, BookingCancelAPIView, BookingListCreateAPIView

urlpatterns = [
    path(
        "",
        BookingListCreateAPIView.as_view(),
        name="booking-list-create",
    ),
    path(
        "<int:pk>/cancel/",
        BookingCancelAPIView.as_view(),
        name="booking-cancel",
    ),
    path(
        "admin/",
        AdminBookingListAPIView.as_view(),
        name="admin-booking-list",
    ),
    path(
        "admin/<int:pk>/manage/",
        AdminBookingManageAPIView.as_view(),
        name="admin-booking-manage",
    ),
]
