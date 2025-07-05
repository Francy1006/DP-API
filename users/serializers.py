from rest_framework import serializers
from .models import User, UserType, UserToken

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'type', 'description', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'code', 'type', 'type_name', 'google_id', 'mail', 'phone',
            'name', 'last_name', 'is_active', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class UserTokenSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_id.name', read_only=True)
    
    class Meta:
        model = UserToken
        fields = [
            'id', 'user_id', 'user_name', 'token', 'ip_address', 'user_agent',
            'created_at', 'expires_at', 'revoked_at'
        ]
        read_only_fields = ['id', 'created_at'] 