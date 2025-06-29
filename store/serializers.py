from rest_framework import serializers
from .models import ItemGroup


class ItemGroupSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemGroup
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'description', 'cataloge_render', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemGroupListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar grupos de items
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'cataloge_render'] 