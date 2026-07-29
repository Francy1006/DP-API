from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "sku",
        "description",
        "provider",
        "type",
        "item_group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
        "created_at",
    ]
    list_filter = [
        "provider",
        "type",
        "item_group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
        "created_at",
    ]
    search_fields = ["code", "sku", "description"]
    ordering = ["description"]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "confirmed_at",
        "deleted_at",
        "log",
        "version",
    ]
    fieldsets = (
        (
            "Información Básica",
            {"fields": ("code", "sku", "description", "obs")},
        ),
        (
            "Clasificación",
            {"fields": ("type", "item_group", "category")},
        ),
        (
            "Proveedor y Precios",
            {
                "fields": (
                    "provider",
                    "price",
                    "package_unit",
                    "min_package_purchase",
                )
            },
        ),
        ("Paquete y URL", {"fields": ("package", "url")}),
        ("Estado", {"fields": ("is_active", "is_deleted", "is_confirmed")}),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "confirmed_at",
                    "deleted_at",
                    "log",
                    "version",
                ),
                "classes": ("collapse",),
            },
        ),
    )
