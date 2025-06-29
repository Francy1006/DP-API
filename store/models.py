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
    cataloge_render = models.BooleanField(
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
    cataloge_render = models.BooleanField(
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


class InstructionType(models.Model):
    """
    Modelo para tipos de instrucciones
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    is_deleted = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Eliminado"
    )
    is_confirmed = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Confirmado"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Eliminación"
    )
    created_by = models.CharField(
        max_length=36,
        verbose_name="Creado por"
    )
    confirmed_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Confirmado por"
    )
    updated_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Actualizado por"
    )
    deleted_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Eliminado por"
    )

    class Meta:
        db_table = 'instruction_type'
        verbose_name = "Tipo de Instrucción"
        verbose_name_plural = "Tipos de Instrucciones"
        ordering = ['type']

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Instruction(models.Model):
    """
    Modelo para instrucciones del sistema
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    instruction = models.CharField(max_length=50, verbose_name="Instrucción")
    description = models.TextField(verbose_name="Descripción")
    url_documentation = models.URLField(
        max_length=2083, 
        null=True, 
        blank=True,
        verbose_name="URL de Documentación"
    )
    type = models.ForeignKey(
        InstructionType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo de Instrucción"
    )
    is_deleted = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Eliminado"
    )
    is_confirmed = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Confirmado"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Eliminación"
    )
    created_by = models.CharField(
        max_length=36,
        verbose_name="Creado por"
    )
    confirmed_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Confirmado por"
    )
    updated_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Actualizado por"
    )
    deleted_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Eliminado por"
    )

    class Meta:
        db_table = 'instruction'
        verbose_name = "Instrucción"
        verbose_name_plural = "Instrucciones"
        ordering = ['-created_at']

    def __str__(self):
        return self.instruction

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Cataloge(models.Model):
    """
    Modelo para catálogo de productos
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        verbose_name="Código"
    )
    sku = models.CharField(max_length=50, verbose_name="SKU")
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        db_column='menu',
        verbose_name="Menú"
    )
    group = models.ForeignKey(
        ItemGroup,
        on_delete=models.CASCADE,
        db_column='group',
        verbose_name="Grupo"
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        db_column='category',
        verbose_name="Categoría"
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo"
    )
    restriction = models.CharField(
        max_length=36,
        verbose_name="Restricción"
    )
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    OBS = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )
    chef_recommendation = models.BooleanField(
        default=False,
        verbose_name="Recomendación del Chef"
    )
    usage_instructions = models.ForeignKey(
        Instruction,
        on_delete=models.CASCADE,
        db_column='usage_instructions',
        verbose_name="Instrucciones de Uso"
    )
    base_gross_price = models.IntegerField(
        default=0,
        verbose_name="Precio Bruto Base"
    )
    min_quantity_purchase = models.IntegerField(
        default=1,
        verbose_name="Cantidad Mínima de Compra"
    )
    rations_quantity = models.IntegerField(
        default=1,
        verbose_name="Cantidad de Raciones"
    )
    cover_image = models.URLField(
        max_length=2083,
        null=True,
        blank=True,
        verbose_name="Imagen de Portada"
    )
    secondary_image = models.URLField(
        max_length=2083,
        null=True,
        blank=True,
        verbose_name="Imagen Secundaria"
    )
    complementary_image = models.URLField(
        max_length=2083,
        null=True,
        blank=True,
        verbose_name="Imagen Complementaria"
    )
    image_gallery = models.URLField(
        max_length=2083,
        null=True,
        blank=True,
        verbose_name="Galería de Imágenes"
    )
    configuration = models.CharField(
        max_length=36,
        verbose_name="Configuración"
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name="Visible"
    )
    is_deleted = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Eliminado"
    )
    is_confirmed = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Confirmado"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Eliminación"
    )
    created_by = models.CharField(
        max_length=36,
        verbose_name="Creado por"
    )
    confirmed_by = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Confirmado por"
    )
    updated_by = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Actualizado por"
    )
    deleted_by = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Eliminado por"
    )
    LOG = models.TextField(verbose_name="Log")
    version = models.IntegerField(
        default=1,
        verbose_name="Versión"
    )

    class Meta:
        db_table = 'cataloge'
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.sku}"

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
