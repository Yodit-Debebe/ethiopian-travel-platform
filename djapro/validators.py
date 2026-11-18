from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def validate_image_size(image):
    if image.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError(
            f"Image size must be {MAX_IMAGE_SIZE_MB} MB or smaller."
        )
