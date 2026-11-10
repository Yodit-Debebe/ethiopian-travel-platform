
from decimal import Decimal
from datetime import date

from rest_framework import serializers

from .models import Booking
from travello.models import Destination


class BookingSerializer(serializers.ModelSerializer):

    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all()
    )

    class Meta:
        model = Booking

        fields = [
            "id",
            "destination",
            "travel_date",
            "number_of_travelers",
            "total_price",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "total_price",
            "status",
            "created_at",
        ]

    def validate_travel_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Travel date cannot be in the past."
            )

        return value

    def validate_number_of_travelers(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "At least one traveler is required."
            )

        return value

    def create(self, validated_data):
        destination = validated_data["destination"]
        number_of_travelers = validated_data["number_of_travelers"]

        total_price = (
            Decimal(str(destination.price)) * number_of_travelers
        )

        return Booking.objects.create(
            user=self.context["request"].user,
            total_price=total_price,
            **validated_data
        )
