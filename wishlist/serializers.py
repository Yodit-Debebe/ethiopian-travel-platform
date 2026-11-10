
from rest_framework import serializers

from .models import Wishlist
from travello.models import Destination


class WishlistSerializer(serializers.ModelSerializer):

    destination_name = serializers.CharField(
        source="destination.name",
        read_only=True
    )

    destination_price = serializers.IntegerField(
        source="destination.price",
        read_only=True
    )

    destination_image = serializers.ImageField(
        source="destination.img",
        read_only=True
    )

    class Meta:
        model = Wishlist

        fields = [
            "id",
            "destination",
            "destination_name",
            "destination_price",
            "destination_image",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_destination(self, destination):

        user = self.context["request"].user

        if Wishlist.objects.filter(
            user=user,
            destination=destination
        ).exists():

            raise serializers.ValidationError(
                "This destination is already in your wishlist."
            )

        return destination
