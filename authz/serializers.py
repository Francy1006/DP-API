from rest_framework import serializers
from .models import Role, Permission, PermissionType, RolePermissions, Restriction, RestrictionRoles

class PermissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PermissionSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Permission
        fields = [
            'id', 'permission', 'description', 'type', 'type_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'updated_by',
            'confirmed_by', 'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id', 'role', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']


class RolePermissionsSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role', read_only=True)
    permission_name = serializers.CharField(source='permission.permission', read_only=True)
    
    class Meta:
        model = RolePermissions
        fields = [
            'id', 'role', 'role_name', 'permission', 'permission_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restriction
        fields = [
            'id', 'restriction', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']


class RestrictionRolesSerializer(serializers.ModelSerializer):
    restriction_name = serializers.CharField(source='restriction.restriction', read_only=True)
    role_name = serializers.CharField(source='role.role', read_only=True)
    
    class Meta:
        model = RestrictionRoles
        fields = [
            'id', 'restriction', 'restriction_name', 'role', 'role_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'] 