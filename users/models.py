from django.db import models
import uuid
from django.utils import timezone

class UserType(models.Model):
    """
    Modelo para tipos de usuario
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'user_type'
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuario"
        ordering = ['type']

    def __str__(self):
        return self.type


class User(models.Model):
    """
    Modelo para usuarios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, db_column='type')
    google_id = models.CharField(max_length=255, unique=True, verbose_name="Google ID")
    mail = models.CharField(max_length=255, unique=True, verbose_name="Email")
    phone = models.BigIntegerField(verbose_name="Teléfono")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido")
    is_active = models.BooleanField(null=True, blank=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} {self.last_name}"


class UserToken(models.Model):
    """
    Modelo para tokens de usuario
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', to_field='code')
    token = models.TextField(verbose_name="Token")
    ip_address = models.CharField(max_length=45, verbose_name="Dirección IP")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Expiración")
    revoked_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Revocación")

    class Meta:
        db_table = 'user_token'
        verbose_name = "Token de Usuario"
        verbose_name_plural = "Tokens de Usuario"
        ordering = ['-created_at']

    def __str__(self):
        return f"Token for {self.user_id}"
