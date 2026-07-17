from rest_framework import serializers

from providers.models import Provider


class ProviderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=10)
    provider = serializers.CharField(max_length=50)
    type = serializers.IntegerField()
    type_name = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(required=False)
    obs_provider = serializers.CharField(allow_blank=True)
    contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_mail = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_phone = serializers.IntegerField(allow_null=True, required=False)
    contact_phone2 = serializers.IntegerField(allow_null=True, required=False)
    website_url = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    obs_contact = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    company_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    company_rut = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    company_activity = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    legal_representative = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    billing_address = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    billing_mail = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    billing_phone = serializers.IntegerField(allow_null=True, required=False)
    company_bank = serializers.IntegerField(allow_null=True, required=False)
    bank_name = serializers.CharField(allow_null=True, read_only=True)
    bank_account_type = serializers.IntegerField(allow_null=True, required=False)
    bank_account_type_name = serializers.CharField(allow_null=True, read_only=True)
    bank_account_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    bank_account_mail = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    dispatch_address = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    dispatch_maps_location = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    obs_dispatch = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    dispatch_district = serializers.IntegerField(allow_null=True, required=False)
    dispatch_district_name = serializers.CharField(allow_null=True, read_only=True)
    dispatch_region = serializers.IntegerField(allow_null=True, required=False)
    dispatch_region_name = serializers.CharField(allow_null=True, read_only=True)
    is_active = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(allow_null=True, required=False)
    is_confirmed = serializers.BooleanField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(allow_null=True, read_only=True)
    confirmed_at = serializers.DateTimeField(allow_null=True, read_only=True)
    deleted_at = serializers.DateTimeField(allow_null=True, read_only=True)
    created_by = serializers.CharField(max_length=36)
    confirmed_by = serializers.CharField(max_length=36, allow_null=True, required=False)
    updated_by = serializers.CharField(max_length=36, allow_null=True, required=False)
    deleted_by = serializers.CharField(max_length=36, allow_null=True, required=False)
    log = serializers.CharField(read_only=True)
    version = serializers.IntegerField(read_only=True)


class ProviderCommandSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.type", read_only=True)
    dispatch_region_name = serializers.CharField(
        source="dispatch_region.region",
        read_only=True,
    )
    dispatch_district_name = serializers.CharField(
        source="dispatch_district.district",
        read_only=True,
    )
    bank_name = serializers.CharField(source="company_bank.bank", read_only=True)
    bank_account_type_name = serializers.CharField(
        source="bank_account_type.type",
        read_only=True,
    )

    class Meta:
        model = Provider
        fields = [
            "id",
            "code",
            "provider",
            "type",
            "type_name",
            "rating",
            "obs_provider",
            "contact_name",
            "contact_mail",
            "contact_phone",
            "contact_phone2",
            "website_url",
            "obs_contact",
            "company_name",
            "company_rut",
            "company_activity",
            "legal_representative",
            "billing_address",
            "billing_mail",
            "billing_phone",
            "company_bank",
            "bank_name",
            "bank_account_type",
            "bank_account_type_name",
            "bank_account_number",
            "bank_account_mail",
            "dispatch_address",
            "dispatch_maps_location",
            "obs_dispatch",
            "dispatch_district",
            "dispatch_district_name",
            "dispatch_region",
            "dispatch_region_name",
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


class ProviderFilterSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_confirmed = serializers.BooleanField(required=False)
    dispatch_region = serializers.IntegerField(required=False)
    dispatch_district = serializers.IntegerField(required=False)
