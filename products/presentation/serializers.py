from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.Serializer):
    """Stable public Product representation. The audit log is intentionally absent."""

    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=36)
    sku = serializers.CharField(max_length=50)
    description = serializers.CharField()
    obs = serializers.CharField()
    package_unit = serializers.IntegerField()
    min_package_purchase = serializers.IntegerField()
    price = serializers.CharField(max_length=36)
    price_gross_amount = serializers.IntegerField(read_only=True)
    provider = serializers.IntegerField()
    provider_name = serializers.CharField(read_only=True)
    type = serializers.IntegerField()
    type_name = serializers.CharField(read_only=True)
    item_group = serializers.IntegerField()
    item_group_name = serializers.CharField(read_only=True)
    category = serializers.IntegerField()
    category_name = serializers.CharField(read_only=True)
    url = serializers.URLField(allow_null=True, allow_blank=True, required=False)
    package = serializers.IntegerField()
    package_description = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(allow_null=True, read_only=True)
    is_confirmed = serializers.BooleanField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(allow_null=True, read_only=True)
    confirmed_at = serializers.DateTimeField(allow_null=True, read_only=True)
    deleted_at = serializers.DateTimeField(allow_null=True, read_only=True)
    created_by = serializers.CharField(max_length=36)
    confirmed_by = serializers.CharField(
        max_length=36, allow_null=True, required=False
    )
    updated_by = serializers.CharField(
        max_length=36, allow_null=True, required=False
    )
    deleted_by = serializers.CharField(
        max_length=36, allow_null=True, read_only=True
    )
    version = serializers.IntegerField(read_only=True)


class ProductCommandSerializer(serializers.ModelSerializer):
    """DRF request adapter preserving the existing relational validation contract."""

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
            "provider",
            "type",
            "item_group",
            "category",
            "url",
            "package",
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


class ProductFilterSerializer(serializers.Serializer):
    provider = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=False)
    item_group = serializers.IntegerField(required=False)
    category = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_confirmed = serializers.BooleanField(required=False)


class DeletedProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField()
    deleted_at = serializers.DateTimeField()
    deleted_by = serializers.CharField(max_length=36)
