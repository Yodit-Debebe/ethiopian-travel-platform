
from django.urls import path

from .views import (
    ReviewListAPIView,
    MyReviewListCreateAPIView,
    MyReviewDetailAPIView,
    AdminReviewListAPIView,
    AdminReviewModerationAPIView,
)


urlpatterns = [

    path(
        "",
        ReviewListAPIView.as_view(),
        name="review-list"
    ),

    path(
        "my/",
        MyReviewListCreateAPIView.as_view(),
        name="my-review-list-create"
    ),

    path(
        "my/<int:pk>/",
        MyReviewDetailAPIView.as_view(),
        name="my-review-detail"
    ),

    path(
        "admin/",
        AdminReviewListAPIView.as_view(),
        name="admin-review-list"
    ),

    path(
        "admin/<int:pk>/moderate/",
        AdminReviewModerationAPIView.as_view(),
        name="admin-review-moderate"
    ),

]
