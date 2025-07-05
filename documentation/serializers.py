from rest_framework import serializers
from .models import InstructionType, Instruction

class InstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Instruction
        fields = [
            'id', 'instruction', 'description', 'url_documentation', 'type', 'type_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'] 