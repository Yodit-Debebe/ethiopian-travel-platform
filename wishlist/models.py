
from django.db import models
from django.contrib.auth.models import User

from travello.models import Destination


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "destination"],
                name="unique_user_wishlist_destination"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
