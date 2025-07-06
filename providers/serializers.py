from rest_framework import serializers
from .models import Provider, ProviderType, ProviderGroup, Region, District, Bank, BankAccountType

class ProviderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ProviderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderGroup
        fields = ['id', 'group_name', 'description', 'catalog_render']
        read_only_fields = ['id']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region', 'description']
        read_only_fields = ['id']


class DistrictSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'district', 'region', 'region_name', 'description']
        read_only_fields = ['id']


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'bank', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class BankAccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ProviderSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    region_name = serializers.CharField(source='dispatch_region.region', read_only=True)
    district_name = serializers.CharField(source='dispatch_district.district', read_only=True)
    bank_name = serializers.CharField(source='company_bank.bank', read_only=True)
    bank_account_type_name = serializers.CharField(source='bank_account_type.type', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'code', 'provider', 'type', 'type_name', 'rating', 'obs_provider',
            'contact_name', 'contact_mail', 'contact_phone', 'contact_phone2',
            'website_url', 'obs_contact', 'company_name', 'company_rut',
            'company_activity', 'legal_representative', 'billing_address',
            'billing_mail', 'billing_phone', 'company_bank', 'bank_name',
            'bank_account_type', 'bank_account_type_name', 'bank_account_number',
            'bank_account_mail', 'dispatch_address', 'dispatch_maps_location',
            'obs_dispatch', 'dispatch_district', 'dispatch_district_name',
            'dispatch_region', 'dispatch_region_name', 'is_active', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'] 