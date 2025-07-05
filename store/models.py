from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Menu(models.Model):
    """
    Modelo para menús del sistema
    """
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50, verbose_name="Menú")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'menu'
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['menu']

    def __str__(self):
        return self.menu


class ItemCategory(models.Model):
    """
    Modelo para categorías de items con catálogo renderizable
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, verbose_name="Categoría")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(
        default=True, 
        verbose_name="Renderizar en Catálogo"
    )

    class Meta:
        db_table = 'item_category'
        verbose_name = "Categoría de Items"
        verbose_name_plural = "Categorías de Items"
        ordering = ['category']

    def __str__(self):
        return self.category


class ItemType(models.Model):
    """
    Modelo para tipos de items
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'item_type'
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Items"
        ordering = ['type']

    def __str__(self):
        return self.type


class ItemGroup(models.Model):
    """
    Modelo para grupos de items con catálogo renderizable
    """
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50, verbose_name="Nombre del Grupo")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(
        default=True, 
        verbose_name="Renderizar en Catálogo"
    )

    class Meta:
        db_table = 'item_group'
        verbose_name = "Grupo de Items"
        verbose_name_plural = "Grupos de Items"
        ordering = ['group_name']

    def __str__(self):
        return self.group_name


class PackageType(models.Model):
    """
    Modelo para tipos de paquetes
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'package_type'
        verbose_name = "Tipo de Paquete"
        verbose_name_plural = "Tipos de Paquetes"
        ordering = ['type']

    def __str__(self):
        return self.type


class TransportType(models.Model):
    """
    Modelo para tipos de transporte
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'transport_type'
        verbose_name = "Tipo de Transporte"
        verbose_name_plural = "Tipos de Transporte"
        ordering = ['type']

    def __str__(self):
        return self.type


class MeasureUnit(models.Model):
    """
    Modelo para unidades de medida
    """
    id = models.AutoField(primary_key=True)
    measure_unit = models.CharField(max_length=50, verbose_name="Unidad de Medida")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'measure_unit'
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ['measure_unit']

    def __str__(self):
        return self.measure_unit


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
        return f"Token {self.id}"


class InstructionType(models.Model):
    """
    Modelo para tipos de instrucciones
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='instruction_types_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='instruction_types_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='instruction_types_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='instruction_types_deleted')

    class Meta:
        db_table = 'instruction_type'
        verbose_name = "Tipo de Instrucción"
        verbose_name_plural = "Tipos de Instrucciones"
        ordering = ['type']

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Instruction(models.Model):
    """
    Modelo para instrucciones del sistema
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID")
    instruction = models.CharField(max_length=50, verbose_name="Instrucción")
    description = models.TextField(verbose_name="Descripción")
    url_documentation = models.URLField(max_length=2083, null=True, blank=True, verbose_name="URL de Documentación")
    type = models.ForeignKey(InstructionType, on_delete=models.CASCADE, db_column='type')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='instructions_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='instructions_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='instructions_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='instructions_deleted')

    class Meta:
        db_table = 'instruction'
        verbose_name = "Instrucción"
        verbose_name_plural = "Instrucciones"
        ordering = ['-created_at']

    def __str__(self):
        return self.instruction

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Package(models.Model):
    """
    Modelo para paquetes
    """
    id = models.AutoField(primary_key=True)
    description = models.TextField(verbose_name="Descripción")
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, db_column='package_type')
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE, db_column='transport_type')
    size = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tamaño")
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Peso")
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, db_column='measure_unit')
    quantity_unit = models.IntegerField(default=1, verbose_name="Cantidad de Unidad")
    storage_instructions = models.ForeignKey(Instruction, on_delete=models.CASCADE, db_column='storage_instructions', related_name='storage_packages')
    transport_instructions = models.ForeignKey(Instruction, on_delete=models.CASCADE, db_column='transport_instructions', related_name='transport_packages')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='packages_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='packages_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='packages_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='packages_deleted')

    class Meta:
        db_table = 'package'
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ['description']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Catalog(models.Model):
    """
    Modelo para catálogo de productos
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='item_group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    restriction = models.CharField(max_length=36, verbose_name="Restricción")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    obs = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones")
    chef_recommendation = models.BooleanField(default=False, verbose_name="Recomendación del Chef")
    usage_instructions = models.ForeignKey(Instruction, on_delete=models.CASCADE, db_column='usage_instructions')
    price = models.CharField(max_length=36, verbose_name="Precio", db_column='base_gross_price')
    min_quantity_purchase = models.IntegerField(default=1, verbose_name="Cantidad Mínima de Compra")
    rations_quantity = models.IntegerField(default=1, verbose_name="Cantidad de Raciones")
    cover_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Complementaria")
    image_gallery = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Galería de Imágenes")
    configuration = models.CharField(max_length=36, verbose_name="Configuración")
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='catalogs_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='catalogs_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='catalogs_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='catalogs_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'catalog'
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


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
        if not self._state.adding:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
