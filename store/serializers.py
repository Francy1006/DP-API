from rest_framework import serializers
from .models import (
    ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, Catalog, Provider,
    PackageType, TransportType, MeasureUnit, ProviderType, BankAccountType, Region, District,
    Bank, UserType, User, UserToken, Package
)


# Menu Serializers
class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Menu
    """
    class Meta:
        model = Menu
        fields = ['id', 'menu', 'description']
        read_only_fields = ['id']


class MenuListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar menús
    """
    class Meta:
        model = Menu
        fields = ['id', 'menu']


# ItemCategory Serializers
class ItemCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemCategory
    """
    class Meta:
        model = ItemCategory
        fields = ['id', 'category', 'description', 'catalog_render']
        read_only_fields = ['id']


class ItemCategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar categorías de items
    """
    class Meta:
        model = ItemCategory
        fields = ['id', 'category', 'catalog_render']


# ItemType Serializers
class ItemTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemType
    """
    class Meta:
        model = ItemType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ItemTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de items
    """
    class Meta:
        model = ItemType
        fields = ['id', 'type']


# ItemGroup Serializers
class ItemGroupSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemGroup
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'description', 'catalog_render']
        read_only_fields = ['id']


class ItemGroupListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar grupos de items
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'catalog_render']


# PackageType Serializers
class PackageTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PackageType
    """
    class Meta:
        model = PackageType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class PackageTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de paquetes
    """
    class Meta:
        model = PackageType
        fields = ['id', 'type']


# TransportType Serializers
class TransportTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TransportType
    """
    class Meta:
        model = TransportType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class TransportTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de transporte
    """
    class Meta:
        model = TransportType
        fields = ['id', 'type']


# MeasureUnit Serializers
class MeasureUnitSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo MeasureUnit
    """
    class Meta:
        model = MeasureUnit
        fields = ['id', 'measure_unit', 'description']
        read_only_fields = ['id']


class MeasureUnitListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar unidades de medida
    """
    class Meta:
        model = MeasureUnit
        fields = ['id', 'measure_unit']


# ProviderType Serializers
class ProviderTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ProviderType
    """
    class Meta:
        model = ProviderType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ProviderTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de proveedores
    """
    class Meta:
        model = ProviderType
        fields = ['id', 'type']


# BankAccountType Serializers
class BankAccountTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo BankAccountType
    """
    class Meta:
        model = BankAccountType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class BankAccountTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de cuenta bancaria
    """
    class Meta:
        model = BankAccountType
        fields = ['id', 'type']


# Region Serializers
class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Region
    """
    class Meta:
        model = Region
        fields = ['id', 'region', 'description']
        read_only_fields = ['id']


class RegionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar regiones
    """
    class Meta:
        model = Region
        fields = ['id', 'region']


# District Serializers
class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo District
    """
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'district', 'region', 'region_name', 'description']
        read_only_fields = ['id']


class DistrictListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar distritos
    """
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'district', 'region_name']


# Bank Serializers
class BankSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Bank
    """
    class Meta:
        model = Bank
        fields = ['id', 'bank', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class BankListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar bancos
    """
    class Meta:
        model = Bank
        fields = ['id', 'bank']


# UserType Serializers
class UserTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserType
    """
    class Meta:
        model = UserType
        fields = ['id', 'type', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de usuario
    """
    class Meta:
        model = UserType
        fields = ['id', 'type']


# User Serializers
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'code', 'type', 'type_name', 'google_id', 'mail', 'phone', 'name', 'last_name',
            'is_active', 'is_deleted', 'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar usuarios
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'code', 'name', 'last_name', 'mail', 'type_name', 'is_active']


# UserToken Serializers
class UserTokenSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserToken
    """
    user_name = serializers.CharField(source='user_id.name', read_only=True)
    
    class Meta:
        model = UserToken
        fields = [
            'id', 'user_id', 'user_name', 'token', 'ip_address', 'user_agent',
            'created_at', 'expires_at', 'revoked_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserTokenListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tokens de usuario
    """
    user_name = serializers.CharField(source='user_id.name', read_only=True)
    
    class Meta:
        model = UserToken
        fields = ['id', 'user_name', 'ip_address', 'created_at', 'expires_at', 'revoked_at']


# InstructionType Serializers
class InstructionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InstructionType
    """
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    deleted_by_name = serializers.CharField(source='deleted_by.name', read_only=True)
    
    class Meta:
        model = InstructionType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'created_by_name', 'confirmed_by', 'confirmed_by_name',
            'updated_by', 'updated_by_name', 'deleted_by', 'deleted_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de instrucciones
    """
    class Meta:
        model = InstructionType
        fields = ['id', 'type', 'is_confirmed']


# Instruction Serializers
class InstructionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Instruction
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    deleted_by_name = serializers.CharField(source='deleted_by.name', read_only=True)
    
    class Meta:
        model = Instruction
        fields = [
            'id', 'instruction', 'description', 'url_documentation', 
            'type', 'type_name', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'created_by_name', 'confirmed_by', 'confirmed_by_name',
            'updated_by', 'updated_by_name', 'deleted_by', 'deleted_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar instrucciones
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model = Instruction
        fields = ['id', 'instruction', 'type_name', 'is_confirmed', 'created_at', 'created_by_name']


class InstructionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear instrucciones (sin campos de auditoría)
    """
    class Meta:
        model = Instruction
        fields = [
            'instruction', 'description', 'url_documentation', 
            'type', 'created_by'
        ]


class InstructionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar instrucciones
    """
    class Meta:
        model = Instruction
        fields = [
            'instruction', 'description', 'url_documentation', 
            'type', 'updated_by'
        ]


# Package Serializers
class PackageSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Package
    """
    package_type_name = serializers.CharField(source='package_type.type', read_only=True)
    transport_type_name = serializers.CharField(source='transport_type.type', read_only=True)
    measure_unit_name = serializers.CharField(source='measure_unit.measure_unit', read_only=True)
    storage_instructions_name = serializers.CharField(source='storage_instructions.instruction', read_only=True)
    transport_instructions_name = serializers.CharField(source='transport_instructions.instruction', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    deleted_by_name = serializers.CharField(source='deleted_by.name', read_only=True)
    
    class Meta:
        model = Package
        fields = [
            'id', 'description', 'package_type', 'package_type_name', 'transport_type', 'transport_type_name',
            'size', 'weight', 'measure_unit', 'measure_unit_name', 'quantity_unit',
            'storage_instructions', 'storage_instructions_name', 'transport_instructions', 'transport_instructions_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'created_by_name', 'confirmed_by', 'confirmed_by_name',
            'updated_by', 'updated_by_name', 'deleted_by', 'deleted_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PackageListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar paquetes
    """
    package_type_name = serializers.CharField(source='package_type.type', read_only=True)
    transport_type_name = serializers.CharField(source='transport_type.type', read_only=True)
    
    class Meta:
        model = Package
        fields = ['id', 'description', 'package_type_name', 'transport_type_name', 'size', 'weight']


# Catalog Serializers
class CatalogSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Catalog
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    usage_instructions_name = serializers.CharField(source='usage_instructions.instruction', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    deleted_by_name = serializers.CharField(source='deleted_by.name', read_only=True)
    
    class Meta:
        model = Catalog
        fields = [
            'id', 'code', 'sku', 'menu', 'menu_name', 'group', 'group_name', 
            'category', 'category_name', 'type', 'type_name', 'restriction',
            'name', 'description', 'obs', 'chef_recommendation', 
            'usage_instructions', 'usage_instructions_name', 'price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'is_deleted', 'is_confirmed', 'created_at', 
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by', 'created_by_name',
            'confirmed_by', 'confirmed_by_name', 'updated_by', 'updated_by_name',
            'deleted_by', 'deleted_by_name', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class CatalogListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar catálogos
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Catalog
        fields = [
            'id', 'sku', 'name', 'menu_name', 'group_name', 'category_name', 
            'type_name', 'chef_recommendation', 'is_visible', 'cover_image', 'created_at'
        ]


class CatalogCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear catálogos (sin campos de auditoría)
    """
    class Meta:
        model = Catalog
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'obs', 'chef_recommendation', 
            'usage_instructions', 'price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'created_by'
        ]


class CatalogUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar catálogos
    """
    class Meta:
        model = Catalog
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'obs', 'chef_recommendation', 
            'usage_instructions', 'price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'updated_by'
        ]


# Provider Serializers
class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Provider
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    company_bank_name = serializers.CharField(source='company_bank.bank', read_only=True)
    bank_account_type_name = serializers.CharField(source='bank_account_type.type', read_only=True)
    dispatch_district_name = serializers.CharField(source='dispatch_district.district', read_only=True)
    dispatch_region_name = serializers.CharField(source='dispatch_region.region', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    confirmed_by_name = serializers.CharField(source='confirmed_by.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.name', read_only=True)
    deleted_by_name = serializers.CharField(source='deleted_by.name', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'code', 'provider', 'type', 'type_name', 'rating', 'obs_provider',
            'contact_name', 'contact_mail', 'contact_phone', 'contact_phone2', 'website_url',
            'obs_contact', 'company_name', 'company_rut', 'company_activity', 'legal_representative',
            'billing_address', 'billing_mail', 'billing_phone', 'company_bank', 'company_bank_name',
            'bank_account_type', 'bank_account_type_name', 'bank_account_number', 'bank_account_mail',
            'dispatch_address', 'dispatch_maps_location', 'obs_dispatch', 'dispatch_district',
            'dispatch_district_name', 'dispatch_region', 'dispatch_region_name', 'is_active',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'created_by_name', 'confirmed_by', 'confirmed_by_name',
            'updated_by', 'updated_by_name', 'deleted_by', 'deleted_by_name', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ProviderListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar proveedores
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'code', 'provider', 'type_name', 'rating', 'contact_name',
            'contact_mail', 'company_name', 'is_active', 'created_at', 'created_by_name'
        ]


class ProviderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear proveedores (sin campos de auditoría)
    """
    class Meta:
        model = Provider
        fields = [
            'provider', 'type', 'rating', 'obs_provider', 'contact_name', 'contact_mail',
            'contact_phone', 'contact_phone2', 'website_url', 'obs_contact', 'company_name',
            'company_rut', 'company_activity', 'legal_representative', 'billing_address',
            'billing_mail', 'billing_phone', 'company_bank', 'bank_account_type',
            'bank_account_number', 'bank_account_mail', 'dispatch_address', 'dispatch_maps_location',
            'obs_dispatch', 'dispatch_district', 'dispatch_region', 'is_active', 'created_by'
        ]


class ProviderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar proveedores
    """
    class Meta:
        model = Provider
        fields = [
            'provider', 'type', 'rating', 'obs_provider', 'contact_name', 'contact_mail',
            'contact_phone', 'contact_phone2', 'website_url', 'obs_contact', 'company_name',
            'company_rut', 'company_activity', 'legal_representative', 'billing_address',
            'billing_mail', 'billing_phone', 'company_bank', 'bank_account_type',
            'bank_account_number', 'bank_account_mail', 'dispatch_address', 'dispatch_maps_location',
            'obs_dispatch', 'dispatch_district', 'dispatch_region', 'is_active', 'updated_by'
        ] 