from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "img")
    search_fields = ("name", "desc")
    list_filter = ("category", "price")
    ordering = ("id",)
    list_per_page = 10