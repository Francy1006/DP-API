from django.db import models
import uuid
from django.utils import timezone
from users.models import User


class BranchType(models.Model):
    """
    Modelo para tipos de sucursal
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    type = models.CharField(max_length=50, unique=True, verbose_name="Tipo")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='branch_types_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='branch_types_updated')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'branch_types'
        verbose_name = "Tipo de Sucursal"
        verbose_name_plural = "Tipos de Sucursal"
        ordering = ['type']

    def __str__(self):
        return self.type


class Branch(models.Model):
    """
    Modelo para sucursales
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    branch = models.CharField(max_length=100, verbose_name="Sucursal")
    description = models.TextField(verbose_name="Descripción")
    type = models.ForeignKey(BranchType, on_delete=models.CASCADE, db_column='type', to_field='code')
    district = models.ForeignKey('providers.District', on_delete=models.CASCADE, db_column='district')
    region = models.ForeignKey('providers.Region', on_delete=models.CASCADE, db_column='region')
    address = models.TextField(verbose_name="Dirección")
    maps_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación en Maps")
    phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono")
    mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email")
    opening_hours = models.CharField(max_length=255, null=True, blank=True, verbose_name="Horario de Apertura")
    tag = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tag")
    cover_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Complementaria")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='branches_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='branches_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='branches_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='branches_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'branches'
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['branch']

    def __str__(self):
        return self.branch

    def save(self, *args, **kwargs):
        if not self.is_confirmed:
            self.is_confirmed = False
        super().save(*args, **kwargs)


class Platform(models.Model):
    """
    Modelo para plataformas
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    platform = models.CharField(max_length=100, unique=True, verbose_name="Plataforma")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sitio Web")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='platforms_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='platforms_updated')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'platform'
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"
        ordering = ['platform']

    def __str__(self):
        return self.platform


class PlatformDetail(models.Model):
    """
    Modelo para detalles de plataforma
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branch', to_field='code')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, db_column='platform', to_field='code')
    param_key = models.CharField(max_length=100, verbose_name="Clave de Parámetro")
    param_value = models.TextField(null=True, blank=True, verbose_name="Valor de Parámetro")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    is_required = models.BooleanField(default=False, verbose_name="Requerido")
    is_encrypted = models.BooleanField(default=False, verbose_name="Encriptado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='platform_details_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='platform_details_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='platform_details_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'platform_detail'
        verbose_name = "Detalle de Plataforma"
        verbose_name_plural = "Detalles de Plataforma"
        ordering = ['branch', 'platform']

    def __str__(self):
        return f"{self.branch} - {self.platform} - {self.param_key}"


class CompanyAgreement(models.Model):
    """
    Modelo para empresas de convenios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    company = models.CharField(max_length=150, verbose_name="Empresa")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='company_agreements_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='company_agreements_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='company_agreements_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'company_agreements'
        verbose_name = "Empresa de Convenio"
        verbose_name_plural = "Empresas de Convenios"
        ordering = ['company']

    def __str__(self):
        return self.company


class Agreement(models.Model):
    """
    Modelo para convenios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    company = models.ForeignKey(CompanyAgreement, on_delete=models.CASCADE, db_column='company', to_field='code')
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Descuento")
    start_date = models.DateField(verbose_name="Fecha de Inicio")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='agreements_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='agreements_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='agreements_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'agreements'
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['company', 'name']

    def __str__(self):
        return f"{self.company} - {self.name}"


class AgreementDetail(models.Model):
    """
    Modelo para detalles de convenio
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    company = models.ForeignKey(CompanyAgreement, on_delete=models.CASCADE, db_column='company', to_field='code')
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, db_column='agreement', to_field='code')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branch', to_field='code')
    ticket = models.ForeignKey('ticket.Ticket', on_delete=models.SET_NULL, null=True, blank=True, db_column='ticket', to_field='code')
    benefit_applied = models.BooleanField(default=False, verbose_name="Beneficio Aplicado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='agreement_details_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='agreement_details_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='agreement_details_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'agreement_detail'
        verbose_name = "Detalle de Convenio"
        verbose_name_plural = "Detalles de Convenios"
        ordering = ['company', 'agreement', 'branch']

    def __str__(self):
        return f"{self.company} - {self.agreement} - {self.branch}"







