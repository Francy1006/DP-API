from django.db import models
import uuid
from django.utils import timezone
from users.models import User

class ProviderType(models.Model):
    """
    Modelo para tipos de proveedores
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'provider_type'
        verbose_name = "Tipo de Proveedor"
        verbose_name_plural = "Tipos de Proveedores"
        ordering = ['type']

    def __str__(self):
        return self.type


class BankAccountType(models.Model):
    """
    Modelo para tipos de cuenta bancaria
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'bank_account_type'
        verbose_name = "Tipo de Cuenta Bancaria"
        verbose_name_plural = "Tipos de Cuenta Bancaria"
        ordering = ['type']

    def __str__(self):
        return self.type


class Region(models.Model):
    """
    Modelo para regiones
    """
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255, verbose_name="Región")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'region'
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        ordering = ['region']

    def __str__(self):
        return self.region


class District(models.Model):
    """
    Modelo para distritos
    """
    id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=255, verbose_name="Distrito")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region')
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'district'
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['district']

    def __str__(self):
        return self.district


class Bank(models.Model):
    """
    Modelo para bancos
    """
    id = models.AutoField(primary_key=True)
    bank = models.CharField(max_length=255, verbose_name="Banco")
    description = models.TextField(verbose_name="Descripción")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'bank'
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"
        ordering = ['bank']

    def __str__(self):
        return self.bank


class Provider(models.Model):
    """
    Modelo para proveedores
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    provider = models.CharField(max_length=50, unique=True, verbose_name="Proveedor")
    type = models.ForeignKey(ProviderType, on_delete=models.CASCADE, db_column='type')
    rating = models.IntegerField(default=0, verbose_name="Calificación")
    obs_provider = models.TextField(verbose_name="Observaciones del Proveedor")
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre de Contacto")
    contact_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Contacto")
    contact_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto")
    contact_phone2 = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto 2")
    website_url = models.TextField(null=True, blank=True, verbose_name="URL del Sitio Web")
    obs_contact = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones de Contacto")
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nombre de la Empresa")
    company_rut = models.CharField(max_length=12, null=True, blank=True, verbose_name="RUT de la Empresa")
    company_activity = models.CharField(max_length=255, null=True, blank=True, verbose_name="Actividad de la Empresa")
    legal_representative = models.CharField(max_length=255, null=True, blank=True, verbose_name="Representante Legal")
    billing_address = models.TextField(null=True, blank=True, verbose_name="Dirección de Facturación")
    billing_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Facturación")
    billing_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Facturación")
    company_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, db_column='company_bank')
    bank_account_type = models.ForeignKey(BankAccountType, on_delete=models.SET_NULL, null=True, blank=True, db_column='bank_account_type')
    bank_account_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número de Cuenta Bancaria")
    bank_account_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Cuenta Bancaria")
    dispatch_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección de Despacho")
    dispatch_maps_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación en Maps")
    obs_dispatch = models.TextField(null=True, blank=True, verbose_name="Observaciones de Despacho")
    dispatch_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_district')
    dispatch_region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_region')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='providers_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='providers_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='providers_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='providers_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'provider'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['provider']

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        if not self.is_confirmed:
            self.is_confirmed = False
        super().save(*args, **kwargs)
