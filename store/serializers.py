from rest_framework import serializers
from .models import ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, Cataloge


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
        fields = ['id', 'category', 'description', 'cataloge_render']
        read_only_fields = ['id']


class ItemCategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar categorías de items
    """
    class Meta:
        model = ItemCategory
        fields = ['id', 'category', 'cataloge_render']


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


# ItemGroup Serializers (existing)
class ItemGroupSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemGroup
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'description', 'cataloge_render']
        read_only_fields = ['id']


class ItemGroupListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar grupos de items
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'cataloge_render']


# InstructionType Serializers
class InstructionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InstructionType
    """
    class Meta:
        model = InstructionType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
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
    
    class Meta:
        model = Instruction
        fields = [
            'id', 'instruction', 'description', 'url_documentation', 
            'type', 'type_name', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar instrucciones
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Instruction
        fields = ['id', 'instruction', 'type_name', 'is_confirmed', 'created_at']


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


# Cataloge Serializers
class CatalogeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cataloge
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Cataloge
        fields = [
            'id', 'sku', 'menu', 'menu_name', 'group', 'group_name', 
            'category', 'category_name', 'type', 'type_name', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'is_deleted', 'is_confirmed', 'created_at', 
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class CatalogeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar catálogos
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Cataloge
        fields = [
            'id', 'sku', 'name', 'menu_name', 'group_name', 'category_name', 
            'type_name', 'is_visible', 'is_confirmed', 'created_at'
        ]


class CatalogeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear catálogos (sin campos de auditoría)
    """
    class Meta:
        model = Cataloge
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'created_by', 'LOG'
        ]


class CatalogeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar catálogos
    """
    class Meta:
        model = Cataloge
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'updated_by', 'LOG'
        ] 