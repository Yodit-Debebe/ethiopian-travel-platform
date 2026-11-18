
from django.core.validators import FileExtensionValidator
from django.db import models

from djapro.validators import (
    ALLOWED_IMAGE_EXTENSIONS,
    validate_image_size,
)


class Destination(models.Model):

    class Category(models.TextChoices):
        HISTORICAL = "HISTORICAL", "Historical Sites"
        NATURAL = "NATURAL", "Natural Attractions"
        LAKE = "LAKE", "Lakes"
        CULTURAL = "CULTURAL", "Cultural Attractions"
        ADVENTURE = "ADVENTURE", "Adventure"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=100)

    desc = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    img = models.ImageField(
        upload_to="pics",
        validators=[
            FileExtensionValidator(ALLOWED_IMAGE_EXTENSIONS),
            validate_image_size,
        ],
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )

    def __str__(self):
        return self.name
