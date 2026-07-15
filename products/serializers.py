from rest_framework import serializers
from .models import (
    Menu,
    ItemCategory,
    ItemType,
    ItemGroup,
    PackageType,
    TransportType,
    MeasureUnit,
    Package,
    Catalog,
    ItemConfiguration,
    ItemConfigurationDetail,
    Product,
    Material,
    Service,
)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "menu", "description", "franchise_only"]
        read_only_fields = ["id"]


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ["id", "category", "description", "catalog_render"]
        read_only_fields = ["id"]


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ["id", "group_name", "description", "catalog_render"]
        read_only_fields = ["id"]


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = ["id", "measure_unit", "description"]
        read_only_fields = ["id"]


class PackageSerializer(serializers.ModelSerializer):
    package_type_name = serializers.CharField(
        source="package_type.type", read_only=True
    )
    transport_type_name = serializers.CharField(
        source="transport_type.type", read_only=True
    )
    measure_unit_name = serializers.CharField(
        source="measure_unit.measure_unit", read_only=True
    )

    class Meta:
        model = Package
        fields = [
            "id",
            "description",
            "package_type",
            "package_type_name",
            "transport_type",
            "transport_type_name",
            "size",
            "weight",
            "measure_unit",
            "measure_unit_name",
            "quantity_unit",
            "storage_instructions",
            "transport_instructions",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class CatalogSerializer(serializers.ModelSerializer):
    menu_name = serializers.CharField(source="menu.menu", read_only=True)
    group_name = serializers.CharField(source="group.group_name", read_only=True)
    category_name = serializers.CharField(source="category.category", read_only=True)
    type_name = serializers.CharField(source="type.type", read_only=True)

    class Meta:
        model = Catalog
        fields = [
            "id",
            "code",
            "sku",
            "name",
            "description",
            "obs",
            "menu",
            "menu_name",
            "group",
            "group_name",
            "category",
            "category_name",
            "type",
            "type_name",
            "restriction",
            "chef_recommendation",
            "usage_instructions",
            "price",
            "min_quantity_purchase",
            "rations_quantity",
            "cover_image",
            "secondary_image",
            "complementary_image",
            "image_gallery",
            "configuration",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "log",
            "version",
        ]


class ItemConfigurationSerializer(serializers.ModelSerializer):
    package_description = serializers.CharField(
        source="package.description", read_only=True
    )

    class Meta:
        model = ItemConfiguration
        fields = [
            "id",
            "code",
            "configuration",
            "description",
            "package",
            "package_description",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "log",
            "version",
        ]


class ItemConfigurationDetailSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.type", read_only=True)
    configuration_name = serializers.CharField(
        source="configuration.configuration", read_only=True
    )

    class Meta:
        model = ItemConfigurationDetail
        fields = [
            "code",
            "detail",
            "type",
            "type_name",
            "configuration",
            "configuration_name",
            "id_item",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
        ]
        read_only_fields = ["created_at", "updated_at", "confirmed_at", "deleted_at"]


class ProductSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(
        source="type.type",
        read_only=True,
    )

    item_group_name = serializers.CharField(
        source="item_group.group_name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.category",
        read_only=True,
    )

    provider_name = serializers.CharField(
        source="provider.provider",
        read_only=True,
    )

    package_description = serializers.CharField(
        source="package.description",
        read_only=True,
    )

    price_gross_amount = serializers.IntegerField(
        source="price.gross_amount",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "price_gross_amount",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "url",
            "package",
            "package_description",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "version",
        ]

        read_only_fields = [
            "id",
            "is_deleted",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "deleted_by",
            "version",
        ]


class MaterialSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.type", read_only=True)
    group_name = serializers.CharField(source="group.group_name", read_only=True)
    category_name = serializers.CharField(source="category.category", read_only=True)
    provider_name = serializers.CharField(source="provider.provider", read_only=True)
    package_description = serializers.CharField(
        source="package.description", read_only=True
    )

    class Meta:
        model = Material
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "group",
            "group_name",
            "category",
            "category_name",
            "url",
            "package",
            "package_description",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "log",
            "version",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.type", read_only=True)
    group_name = serializers.CharField(source="group.group_name", read_only=True)
    category_name = serializers.CharField(source="category.category", read_only=True)
    provider_name = serializers.CharField(source="provider.provider", read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "group",
            "group_name",
            "category",
            "category_name",
            "url",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "log",
            "version",
        ]
