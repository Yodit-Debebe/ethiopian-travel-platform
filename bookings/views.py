
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser


class BookingListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .select_related("destination")
            .order_by("-created_at")
        )


class BookingCancelAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        booking = get_object_or_404(
            Booking,
            pk=pk,
            user=request.user
        )

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {
                    "error": "Only pending bookings can be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.CANCELLED
        booking.save(update_fields=["status", "updated_at"])

        serializer = BookingSerializer(booking)

        return Response(
            {
                "message": "Booking cancelled successfully.",
                "booking": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminBookingListAPIView(generics.ListAPIView):

    queryset = (
        Booking.objects
        .select_related("user", "destination")
        .all()
        .order_by("-created_at")
    )

    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]


class AdminBookingManageAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        booking = get_object_or_404(Booking, pk=pk)

        new_status = request.data.get("status")

        allowed_statuses = [
            Booking.BookingStatus.CONFIRMED,
            Booking.BookingStatus.CANCELLED,
        ]

        if new_status not in allowed_statuses:
            return Response(
                {
                    "error": "Status must be CONFIRMED or CANCELLED."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {
                    "error": "Only pending bookings can be managed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = new_status
        booking.save(update_fields=["status", "updated_at"])

        serializer = BookingSerializer(booking)

        return Response(
            {
                "message": f"Booking {new_status.lower()} successfully.",
                "booking": serializer.data
            },
            status=status.HTTP_200_OK
        )



