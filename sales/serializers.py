from rest_framework import serializers
from .models import (
    Sale, SaleType, SaleCategory, SaleSubcategory,
    SaleBrand, SaleModel, SaleImage, SaleVideo,
    SaleDocument, SaleSpecification, SaleSpecificationType,
    SaleSpecificationValue, SaleSpecificationValueType,
    SaleSpecificationValueUnit, SaleSpecificationValueUnitType
)

# Esta app está preparada para futuras implementaciones de ventas
# Por ahora se mantiene vacía pero con la estructura base

class SalesBaseSerializer(serializers.ModelSerializer):
    """
    Serializer base para entidades de ventas
    """
    class Meta:
        model = None
        fields = []

class SaleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleCategory
        fields = [
            'id', 'category', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category', read_only=True)
    
    class Meta:
        model = SaleSubcategory
        fields = [
            'id', 'subcategory', 'description', 'category', 'category_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleBrand
        fields = [
            'id', 'brand', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.brand', read_only=True)
    
    class Meta:
        model = SaleModel
        fields = [
            'id', 'model', 'description', 'brand', 'brand_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleImage
        fields = [
            'id', 'sale', 'image', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleVideo
        fields = [
            'id', 'sale', 'video', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDocument
        fields = [
            'id', 'sale', 'document', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleSpecificationType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = SaleSpecification
        fields = [
            'id', 'specification', 'description', 'type', 'type_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationValueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleSpecificationValueType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationValueUnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleSpecificationValueUnitType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationValueUnitSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = SaleSpecificationValueUnit
        fields = [
            'id', 'unit', 'description', 'type', 'type_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSpecificationValueSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    unit_name = serializers.CharField(source='unit.unit', read_only=True)
    
    class Meta:
        model = SaleSpecificationValue
        fields = [
            'id', 'value', 'description', 'type', 'type_name', 'unit', 'unit_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class SaleSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.subcategory', read_only=True)
    brand_name = serializers.CharField(source='brand.brand', read_only=True)
    model_name = serializers.CharField(source='model.model', read_only=True)
    
    class Meta:
        model = Sale
        fields = [
            'id', 'code', 'name', 'description', 'type', 'type_name',
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'brand', 'brand_name', 'model', 'model_name', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by',
            'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'] 