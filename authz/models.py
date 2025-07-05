from django.db import models
import uuid
from django.utils import timezone
from users.models import User

class PermissionType(models.Model):
    """
    Modelo para tipos de permisos
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='permission_types_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='permission_types_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='permission_types_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='permission_types_deleted')

    class Meta:
        db_table = 'permission_type'
        verbose_name = "Tipo de Permiso"
        verbose_name_plural = "Tipos de Permisos"
        ordering = ['type']

    def __str__(self):
        return self.type


class Permission(models.Model):
    """
    Modelo para permisos del sistema
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    permission = models.CharField(max_length=50, unique=True, verbose_name="Permiso")
    description = models.TextField(verbose_name="Descripción")
    type = models.ForeignKey(PermissionType, on_delete=models.CASCADE, db_column='type')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='permissions_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='permissions_updated')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='permissions_confirmed')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='permissions_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'permission'
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        ordering = ['permission']

    def __str__(self):
        return self.permission


class Role(models.Model):
    """
    Modelo para roles del sistema
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    role = models.CharField(max_length=50, unique=True, verbose_name="Rol")
    description = models.TextField(verbose_name="Descripción")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='roles_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='roles_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='roles_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='roles_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'role'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['role']

    def __str__(self):
        return self.role


class RolePermissions(models.Model):
    """
    Modelo para relación muchos a muchos entre roles y permisos
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permission')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='role_permissions_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='role_permissions_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='role_permissions_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='role_permissions_deleted')

    class Meta:
        db_table = 'role_permissions'
        verbose_name = "Permiso de Rol"
        verbose_name_plural = "Permisos de Roles"
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role} - {self.permission}"


class Restriction(models.Model):
    """
    Modelo para restricciones del sistema
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    restriction = models.CharField(max_length=50, unique=True, verbose_name="Restricción")
    description = models.TextField(verbose_name="Descripción")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='restrictions_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='restrictions_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='restrictions_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='restrictions_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'restriction'
        verbose_name = "Restricción"
        verbose_name_plural = "Restricciones"
        ordering = ['restriction']

    def __str__(self):
        return self.restriction


class RestrictionRoles(models.Model):
    """
    Modelo para relación muchos a muchos entre restricciones y roles
    """
    id = models.AutoField(primary_key=True)
    restriction = models.ForeignKey(Restriction, on_delete=models.CASCADE, db_column='restriction')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='restriction_roles_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='restriction_roles_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='restriction_roles_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='restriction_roles_deleted')

    class Meta:
        db_table = 'restriction_roles'
        verbose_name = "Rol de Restricción"
        verbose_name_plural = "Roles de Restricciones"
        unique_together = ['restriction', 'role']

    def __str__(self):
        return f"{self.restriction} - {self.role}"
