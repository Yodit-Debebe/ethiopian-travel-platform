
from datetime import date

from rest_framework import serializers

from .models import Review
from bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    destination_name = serializers.CharField(
        source="destination.name",
        read_only=True
    )

    class Meta:
        model = Review

        fields = [
            "id",
            "booking",
            "username",
            "destination",
            "destination_name",
            "rating",
            "comment",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "destination",
            "destination_name",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):

        request = self.context["request"]

        if booking.user != request.user:
            raise serializers.ValidationError(
                "You cannot review another customer's booking."
            )

        if booking.status != Booking.BookingStatus.CONFIRMED:
            raise serializers.ValidationError(
                "Only confirmed bookings can be reviewed."
            )

        if booking.travel_date >= date.today():
            raise serializers.ValidationError(
                "You can only review a trip after its travel date."
            )

        if not booking.payments.filter(
            status="SUCCESSFUL"
        ).exists():
            raise serializers.ValidationError(
                "A successful payment is required to submit a review."
            )

        if Review.objects.filter(booking=booking).exists():
            raise serializers.ValidationError(
                "You have already reviewed this booking."
            )

        return booking

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value

    def validate_comment(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Review comment cannot be empty."
            )

        return value.strip()

    def create(self, validated_data):

        booking = validated_data["booking"]

        return Review.objects.create(
            user=self.context["request"].user,
            destination=booking.destination,
            **validated_data
        )
