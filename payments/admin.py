
from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "booking",
        "amount",
        "payment_method",
        "status",
        "transaction_reference",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "booking__user__username",
        "transaction_reference",
    )

    readonly_fields = (
        "transaction_reference",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
