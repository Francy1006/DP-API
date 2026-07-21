from decimal import Decimal

from rest_framework import serializers

from products.models import Material


class MaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=36)
    sku = serializers.CharField(max_length=50, read_only=True)
    description = serializers.CharField()
    obs = serializers.CharField()
    package_unit = serializers.IntegerField()
    min_package_purchase = serializers.IntegerField()
    price = serializers.CharField(max_length=36, allow_null=True, read_only=True)
    base_net_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    net_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    gross_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    iva_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    aditional_tax_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    retention_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        read_only=True,
        coerce_to_string=False,
    )
    price_configuration = serializers.CharField(
        max_length=36,
        allow_null=True,
        read_only=True,
    )
    price_configuration_label = serializers.CharField(
        allow_null=True,
        read_only=True,
    )
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
        max_length=36,
        allow_null=True,
        read_only=True,
    )
    updated_by = serializers.CharField(
        max_length=36,
        allow_null=True,
        required=False,
    )
    deleted_by = serializers.CharField(
        max_length=36,
        allow_null=True,
        read_only=True,
    )
    version = serializers.IntegerField(read_only=True)


class MaterialCommandSerializer(serializers.ModelSerializer):
    base_net_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
        max_value=Decimal("999999999999.99"),
        required=True,
        write_only=True,
    )
    price_configuration = serializers.CharField(
        max_length=36,
        required=True,
        write_only=True,
    )

    protected_price_fields = {
        "price",
        "net_amount",
        "gross_amount",
        "iva_amount",
        "aditional_tax_amount",
        "retention_amount",
        "record_item_code",
        "price_record_type",
        "is_current",
    }

    def to_internal_value(self, data):
        forbidden = self.protected_price_fields.intersection(data)
        if forbidden:
            raise serializers.ValidationError(
                {
                    field_name: "Este campo de precio no puede modificarse."
                    for field_name in sorted(forbidden)
                }
            )
        return super().to_internal_value(data)

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
            "base_net_amount",
            "price_configuration",
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
            "sku",
            "price",
            "is_deleted",
            "created_at",
            "updated_at",
            "confirmed_at",
            "confirmed_by",
            "deleted_at",
            "deleted_by",
            "version",
        ]


class MaterialFilterSerializer(serializers.Serializer):
    provider = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=False)
    item_group = serializers.IntegerField(required=False)
    category = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_confirmed = serializers.BooleanField(required=False)


class DeletedMaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField()
    deleted_at = serializers.DateTimeField()
    deleted_by = serializers.CharField(max_length=36)
