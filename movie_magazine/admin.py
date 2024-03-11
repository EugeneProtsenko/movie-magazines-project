from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Critic, Magazine, Topic


@admin.register(Critic)
class CriticAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    search_fields = ("topic",)
    list_filter = ("title",)


admin.site.register(Topic)
