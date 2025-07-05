from django.db import models
import uuid
from django.utils import timezone
from users.models import User
from documentation.models import Instruction

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
        if not self.is_confirmed:
            self.is_confirmed = False
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
        if not self.is_confirmed:
            self.is_confirmed = False
        super().save(*args, **kwargs)


class ItemConfiguration(models.Model):
    """
    Modelo para configuraciones de items
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    configuration = models.CharField(max_length=50, verbose_name="Configuración")
    description = models.TextField(verbose_name="Descripción")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, db_column='package')
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='item_configurations_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='item_configurations_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='item_configurations_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='item_configurations_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'item_configuration'
        verbose_name = "Configuración de Item"
        verbose_name_plural = "Configuraciones de Items"
        ordering = ['configuration']

    def __str__(self):
        return self.configuration


class ItemConfigurationDetail(models.Model):
    """
    Modelo para detalles de configuración de items
    """
    code = models.CharField(max_length=36, verbose_name="Código")
    detail = models.CharField(max_length=50, verbose_name="Detalle")
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    configuration = models.ForeignKey(ItemConfiguration, on_delete=models.CASCADE, db_column='configuration', to_field='code')
    id_item = models.CharField(max_length=36, verbose_name="ID del Item")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='item_configuration_details_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='item_configuration_details_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='item_configuration_details_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='item_configuration_details_deleted')

    class Meta:
        db_table = 'item_configuration_detail'
        verbose_name = "Detalle de Configuración de Item"
        verbose_name_plural = "Detalles de Configuración de Items"
        unique_together = ['code', 'type', 'id_item']

    def __str__(self):
        return f"{self.configuration} - {self.detail}"


class Product(models.Model):
    """
    Modelo para productos
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, db_column='provider', to_field='code')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, db_column='package')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='products_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='products_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='products_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='products_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'product'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['description']

    def __str__(self):
        return self.description


class Material(models.Model):
    """
    Modelo para materiales
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, db_column='provider', to_field='code')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, db_column='package')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='materials_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='materials_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='materials_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='materials_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'material'
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['description']

    def __str__(self):
        return self.description


class Service(models.Model):
    """
    Modelo para servicios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, db_column='provider', to_field='code')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='services_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='services_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='services_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='services_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'service'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['description']

    def __str__(self):
        return self.description
