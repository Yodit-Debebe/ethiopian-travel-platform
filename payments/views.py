
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Payment.objects
            .filter(booking__user=self.request.user)
            .select_related(
                "booking",
                "booking__user",
                "booking__destination"
            )
        )


class PaymentSimulationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):

        payment = get_object_or_404(
            Payment.objects.select_for_update(),
            pk=pk,
            booking__user=request.user
        )

        if payment.status != Payment.PaymentStatus.PENDING:
            return Response(
                {
                    "error": "Only pending payments can be processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = request.data.get("result")

        allowed_results = [
            Payment.PaymentStatus.SUCCESSFUL,
            Payment.PaymentStatus.FAILED,
        ]

        if result not in allowed_results:
            return Response(
                {
                    "error": "Result must be SUCCESSFUL or FAILED."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = result

        payment.save(update_fields=["status", "updated_at"])

        serializer = PaymentSerializer(payment)

        return Response(
            {
                "message": f"Payment {result.lower()} successfully.",
                "payment": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminPaymentListAPIView(generics.ListAPIView):

    queryset = (
        Payment.objects
        .select_related(
            "booking",
            "booking__user",
            "booking__destination"
        )
        .all()
    )

    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]


class AdminPaymentRefundAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, pk):

        payment = get_object_or_404(
            Payment.objects.select_for_update(),
            pk=pk
        )

        if payment.status != Payment.PaymentStatus.SUCCESSFUL:
            return Response(
                {
                    "error": "Only successful payments can be refunded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = Payment.PaymentStatus.REFUNDED

        payment.save(update_fields=["status", "updated_at"])

        serializer = PaymentSerializer(payment)

        return Response(
            {
                "message": "Payment refunded successfully.",
                "payment": serializer.data
            },
            status=status.HTTP_200_OK
        )
