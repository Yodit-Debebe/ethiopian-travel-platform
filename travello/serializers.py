
from django.db.models import Avg, Count, Q
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
            "average_rating",
            "review_count",
        ]

    def get_average_rating(self, obj):

        statistics = obj.reviews.filter(
            status="APPROVED"
        ).aggregate(
            average=Avg("rating")
        )

        average = statistics["average"]

        return round(average, 2) if average is not None else 0

    def get_review_count(self, obj):

        return obj.reviews.filter(
            status="APPROVED"
        ).count()
