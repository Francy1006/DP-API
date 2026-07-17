from rest_framework import serializers
from .models import ProviderType, ProviderGroup, Region, District, Bank, BankAccountType
from .presentation.serializers import ProviderSerializer

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
