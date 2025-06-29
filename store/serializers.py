from rest_framework import serializers
from .models import ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction


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