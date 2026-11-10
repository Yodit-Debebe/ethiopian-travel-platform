
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer


class ReviewListAPIView(generics.ListAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    queryset = (
        Review.objects
        .filter(status=Review.ModerationStatus.APPROVED)
        .select_related("user", "destination", "booking")
    )

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):

        queryset = super().get_queryset()

        destination_id = self.request.query_params.get(
            "destination"
        )

        if destination_id is not None:
            if not destination_id.isdigit():
                from rest_framework.exceptions import ValidationError
                raise ValidationError({
                    "destination": "Destination ID must be a positive integer."
                })

            queryset = queryset.filter(
                destination_id=destination_id
            )

        return queryset


class MyReviewListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            Review.objects
            .filter(user=self.request.user)
            .select_related("user", "destination", "booking")
        )


class MyReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):

        return Review.objects.filter(
            user=self.request.user
        )


class AdminReviewListAPIView(generics.ListAPIView):

    queryset = (
        Review.objects
        .select_related("user", "destination", "booking")
        .all()
    )

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]


class AdminReviewModerationAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, pk):

        review = get_object_or_404(
            Review.objects.select_for_update(),
            pk=pk
        )

        new_status = request.data.get("status")

        allowed_statuses = [
            Review.ModerationStatus.APPROVED,
            Review.ModerationStatus.REJECTED,
        ]

        if new_status not in allowed_statuses:
            return Response(
                {
                    "error": "Status must be APPROVED or REJECTED."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if review.status != Review.ModerationStatus.PENDING:
            return Response(
                {
                    "error": "Only pending reviews can be moderated."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        review.status = new_status

        review.save(update_fields=["status", "updated_at"])

        return Response(
            {
                "message": f"Review {new_status.lower()} successfully.",
                "review": ReviewSerializer(review).data
            },
            status=status.HTTP_200_OK
        )
