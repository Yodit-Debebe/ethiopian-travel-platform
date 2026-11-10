
from django.db import models


class Destination(models.Model):

    class Category(models.TextChoices):
        HISTORICAL = "HISTORICAL", "Historical Sites"
        NATURAL = "NATURAL", "Natural Attractions"
        LAKE = "LAKE", "Lakes"
        CULTURAL = "CULTURAL", "Cultural Attractions"
        ADVENTURE = "ADVENTURE", "Adventure"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=25)

    desc = models.TextField()

    price = models.IntegerField()

    img = models.ImageField(upload_to="pics")

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )

    def __str__(self):
        return self.name
