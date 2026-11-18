from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "destination",
        "travel_date",
        "number_of_travelers",
        "total_price",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "travel_date",
        "created_at",
    )

    search_fields = (
        "user__username",
        "destination__name",
    )

    list_select_related = ("user", "destination")

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )