from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "has_picture",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username", "user__email")
    list_select_related = ("user",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="Picture")
    def has_picture(self, obj):
        return bool(obj.profile_picture)
