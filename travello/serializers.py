
from django.db.models import Avg
from rest_framework import serializers

from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination

        fields = [
            "id",
            "name",
            "desc",
            "price",
            "img",
            "category",
            "average_rating",
            "review_count",
        ]

    def get_average_rating(self, obj):

        if hasattr(obj, "average_rating"):
            average = obj.average_rating
        else:
            average = obj.reviews.filter(
                status="APPROVED"
            ).aggregate(
                average=Avg("rating")
            )["average"]

        return round(average, 2) if average is not None else 0

    def get_review_count(self, obj):

        if hasattr(obj, "review_count"):
            return obj.review_count

        return obj.reviews.filter(
            status="APPROVED"
        ).count()
