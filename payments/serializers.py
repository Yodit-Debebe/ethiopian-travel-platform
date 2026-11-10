
from rest_framework import serializers

from .models import Payment
from bookings.models import Booking


class PaymentSerializer(serializers.ModelSerializer):

    booking = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all()
    )

    customer = serializers.CharField(
        source="booking.user.username",
        read_only=True
    )

    class Meta:
        model = Payment

        fields = [
            "id",
            "booking",
            "customer",
            "amount",
            "payment_method",
            "status",
            "transaction_reference",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer",
            "amount",
            "status",
            "transaction_reference",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):

        request = self.context["request"]

        if booking.user != request.user:
            raise serializers.ValidationError(
                "You cannot pay for another customer's booking."
            )

        if booking.status != Booking.BookingStatus.CONFIRMED:
            raise serializers.ValidationError(
                "Only confirmed bookings can be paid for."
            )

        active_payment_exists = Payment.objects.filter(
            booking=booking,
            status__in=[
                Payment.PaymentStatus.PENDING,
                Payment.PaymentStatus.SUCCESSFUL,
            ]
        ).exists()

        if active_payment_exists:
            raise serializers.ValidationError(
                "An active payment already exists for this booking."
            )

        return booking

    def create(self, validated_data):

        booking = validated_data["booking"]

        return Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_method=validated_data["payment_method"]
        )
