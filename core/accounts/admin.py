from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ("email",)
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    search_fields = ("email",)

    fieldsets = (
        (
            "Authentications",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Informations",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        ("Times and Date", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            "Informations",
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
