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
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
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
        related_name='cataloges',
        verbose_name="Grupo"
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        db_column='category',
        related_name='cataloges',
        verbose_name="Categoría"
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        related_name='cataloge_items',
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
        related_name='usage_cataloges',
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


class Restriction(models.Model):
    """
    Modelo para restricciones del sistema
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    restriction = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Restricción"
    )
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
    LOG = models.TextField(verbose_name="Log")
    version = models.IntegerField(
        default=1,
        verbose_name="Versión"
    )

    class Meta:
        db_table = 'restriction'
        verbose_name = "Restricción"
        verbose_name_plural = "Restricciones"
        ordering = ['restriction']

    def __str__(self):
        return self.restriction

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class PermissionType(models.Model):
    """
    Modelo para tipos de permisos
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Nombre del Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'permission_type'
        verbose_name = "Tipo de Permiso"
        verbose_name_plural = "Tipos de Permisos"
        ordering = ['name']

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    Modelo para permisos del sistema
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    permission = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Permiso"
    )
    description = models.TextField(verbose_name="Descripción")
    type = models.ForeignKey(
        PermissionType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo de Permiso"
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
    updated_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Actualizado por"
    )
    confirmed_by = models.CharField(
        max_length=36,
        null=True, 
        blank=True,
        verbose_name="Confirmado por"
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
        db_table = 'permission'
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        ordering = ['permission']

    def __str__(self):
        return self.permission

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Role(models.Model):
    """
    Modelo para roles del sistema
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    role = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Rol"
    )
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
    LOG = models.TextField(verbose_name="Log")
    version = models.IntegerField(
        default=1,
        verbose_name="Versión"
    )

    class Meta:
        db_table = 'role'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['role']

    def __str__(self):
        return self.role

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class RestrictionRoles(models.Model):
    """
    Modelo para relación entre restricciones y roles
    """
    id = models.AutoField(primary_key=True)
    restriction = models.ForeignKey(
        Restriction,
        on_delete=models.CASCADE,
        db_column='restriction',
        verbose_name="Restricción"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        db_column='role',
        related_name='restriction_roles',
        verbose_name="Rol"
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
        db_table = 'restriction_roles'
        verbose_name = "Restricción-Rol"
        verbose_name_plural = "Restricciones-Roles"
        unique_together = ['restriction', 'role']
        ordering = ['restriction', 'role']

    def __str__(self):
        return f"{self.restriction} - {self.role}"

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class RolePermissions(models.Model):
    """
    Modelo para relación entre roles y permisos
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        db_column='role',
        related_name='role_permissions',
        verbose_name="Rol"
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        db_column='permission',
        verbose_name="Permiso"
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
        db_table = 'role_permissions'
        verbose_name = "Rol-Permiso"
        verbose_name_plural = "Roles-Permisos"
        unique_together = ['role', 'permission']
        ordering = ['role', 'permission']

    def __str__(self):
        return f"{self.role} - {self.permission}"

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


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
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column='region',
        related_name='districts',
        verbose_name="Región"
    )
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
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )

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
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        db_table = 'user_type'
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuario"
        ordering = ['type']

    def __str__(self):
        return self.type


class User(models.Model):
    """
    Modelo para usuarios del sistema
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    type = models.ForeignKey(
        UserType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo de Usuario"
    )
    google_id = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name="Google ID"
    )
    mail = models.EmailField(
        max_length=255, 
        unique=True,
        verbose_name="Email"
    )
    phone = models.BigIntegerField(verbose_name="Teléfono")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido")
    is_active = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Activo"
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
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['name', 'last_name']

    def __str__(self):
        return f"{self.name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class UserToken(models.Model):
    """
    Modelo para tokens de usuario
    """
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4,
        verbose_name="ID"
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name="Usuario"
    )
    token = models.TextField(verbose_name="Token")
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    user_agent = models.TextField(
        null=True, 
        blank=True,
        verbose_name="User Agent"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Creación"
    )
    expires_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Expiración"
    )
    revoked_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de Revocación"
    )

    class Meta:
        db_table = 'user_token'
        verbose_name = "Token de Usuario"
        verbose_name_plural = "Tokens de Usuario"
        ordering = ['-created_at']

    def __str__(self):
        return f"Token {self.user_id} - {self.created_at}"


class Package(models.Model):
    """
    Modelo para paquetes
    """
    id = models.AutoField(primary_key=True)
    description = models.TextField(verbose_name="Descripción")
    package_type = models.ForeignKey(
        PackageType,
        on_delete=models.CASCADE,
        db_column='package_type',
        verbose_name="Tipo de Paquete"
    )
    transport_type = models.ForeignKey(
        TransportType,
        on_delete=models.CASCADE,
        db_column='transport_type',
        verbose_name="Tipo de Transporte"
    )
    size = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name="Tamaño"
    )
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name="Peso"
    )
    measure_unit = models.ForeignKey(
        MeasureUnit,
        on_delete=models.CASCADE,
        db_column='measure_unit',
        verbose_name="Unidad de Medida"
    )
    quantity_unit = models.IntegerField(
        default=1,
        verbose_name="Cantidad de Unidades"
    )
    storage_instructions = models.ForeignKey(
        Instruction,
        on_delete=models.CASCADE,
        db_column='storage_instructions',
        related_name='storage_packages',
        verbose_name="Instrucciones de Almacenamiento"
    )
    transport_instructions = models.ForeignKey(
        Instruction,
        on_delete=models.CASCADE,
        db_column='transport_instructions',
        related_name='transport_packages',
        verbose_name="Instrucciones de Transporte"
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
        db_table = 'package'
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ['description']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class ItemConfiguration(models.Model):
    """
    Modelo para configuraciones de items
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    configuration = models.CharField(max_length=50, verbose_name="Configuración")
    description = models.TextField(verbose_name="Descripción")
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        db_column='package',
        related_name='item_configurations',
        verbose_name="Paquete"
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
        db_table = 'item_configuration'
        verbose_name = "Configuración de Item"
        verbose_name_plural = "Configuraciones de Items"
        ordering = ['configuration']

    def __str__(self):
        return self.configuration

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class ItemConfigurationDetail(models.Model):
    """
    Modelo para detalles de configuración de items
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, verbose_name="Código")
    detail = models.CharField(max_length=50, verbose_name="Detalle")
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        related_name='item_configuration_detail_type',
        verbose_name="Tipo"
    )
    configuration = models.ForeignKey(
        ItemConfiguration,
        on_delete=models.CASCADE,
        db_column='configuration',
        verbose_name="Configuración"
    )
    id_item = models.CharField(max_length=36, verbose_name="ID del Item")
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
        db_table = 'item_configuration_detail'
        verbose_name = "Detalle de Configuración"
        verbose_name_plural = "Detalles de Configuración"
        ordering = ['configuration', 'detail']

    def __str__(self):
        return f"{self.configuration} - {self.detail}"

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Provider(models.Model):
    """
    Modelo para proveedores
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    provider = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Proveedor"
    )
    type = models.ForeignKey(
        ProviderType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo de Proveedor"
    )
    rating = models.IntegerField(
        default=0,
        verbose_name="Calificación"
    )
    OBS_provider = models.TextField(verbose_name="Observaciones del Proveedor")
    contact_name = models.CharField(
        max_length=100,
        null=True, 
        blank=True,
        verbose_name="Nombre de Contacto"
    )
    contact_mail = models.EmailField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Email de Contacto"
    )
    contact_phone = models.BigIntegerField(
        null=True, 
        blank=True,
        verbose_name="Teléfono de Contacto"
    )
    contact_phone2 = models.BigIntegerField(
        null=True, 
        blank=True,
        verbose_name="Teléfono de Contacto 2"
    )
    website_url = models.URLField(
        null=True, 
        blank=True,
        verbose_name="URL del Sitio Web"
    )
    OBS_contact = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Observaciones de Contacto"
    )
    company_name = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Nombre de la Empresa"
    )
    company_rut = models.CharField(
        max_length=12,
        null=True, 
        blank=True,
        verbose_name="RUT de la Empresa"
    )
    company_activity = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Actividad de la Empresa"
    )
    legal_representative = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Representante Legal"
    )
    billing_address = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Dirección de Facturación"
    )
    billing_mail = models.EmailField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Email de Facturación"
    )
    billing_phone = models.BigIntegerField(
        null=True, 
        blank=True,
        verbose_name="Teléfono de Facturación"
    )
    company_bank = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        db_column='company_bank',
        verbose_name="Banco de la Empresa"
    )
    bank_account_type = models.ForeignKey(
        BankAccountType,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        db_column='bank_account_type',
        verbose_name="Tipo de Cuenta Bancaria"
    )
    bank_account_number = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Número de Cuenta Bancaria"
    )
    bank_account_mail = models.EmailField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Email de Cuenta Bancaria"
    )
    dispatch_address = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Dirección de Despacho"
    )
    dispatch_maps_location = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="Ubicación en Maps"
    )
    OBS_dispatch = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Observaciones de Despacho"
    )
    dispatch_district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        db_column='dispatch_district',
        verbose_name="Distrito de Despacho"
    )
    dispatch_region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        db_column='dispatch_region',
        related_name='provider_dispatch_region',
        verbose_name="Región de Despacho"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
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
        db_table = 'provider'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['provider']

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Modelo para productos
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    OBS = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    gross_price = models.IntegerField(
        default=0,
        verbose_name="Precio Bruto"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        db_column='provider',
        related_name='products',
        verbose_name="Proveedor"
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        related_name='product_type',
        verbose_name="Tipo"
    )
    group = models.ForeignKey(
        ItemGroup,
        on_delete=models.CASCADE,
        db_column='group',
        related_name='product_group',
        verbose_name="Grupo"
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        db_column='category',
        related_name='product_category',
        verbose_name="Categoría"
    )
    url = models.URLField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="URL"
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        db_column='package',
        related_name='product_packages',
        verbose_name="Paquete"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
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
        db_table = 'product'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['description']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Material(models.Model):
    """
    Modelo para materiales
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    OBS = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    gross_price = models.IntegerField(
        default=0,
        verbose_name="Precio Bruto"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        db_column='provider',
        related_name='materials',
        verbose_name="Proveedor"
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        related_name='material_type',
        verbose_name="Tipo"
    )
    group = models.ForeignKey(
        ItemGroup,
        on_delete=models.CASCADE,
        db_column='group',
        related_name='material_group',
        verbose_name="Grupo"
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        db_column='category',
        related_name='material_category',
        verbose_name="Categoría"
    )
    url = models.URLField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="URL"
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        db_column='package',
        related_name='material_packages',
        verbose_name="Paquete"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
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
        db_table = 'material'
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['description']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Service(models.Model):
    """
    Modelo para servicios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True,
        null=True,  # Permitir null para que MySQL genere el UUID
        blank=True,  # Permitir blank en formularios
        verbose_name="Código"
    )
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    OBS = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Paquete")
    gross_price = models.IntegerField(
        default=0,
        verbose_name="Precio Bruto"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        db_column='provider',
        related_name='services',
        verbose_name="Proveedor"
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='type',
        related_name='service_type',
        verbose_name="Tipo"
    )
    group = models.ForeignKey(
        ItemGroup,
        on_delete=models.CASCADE,
        db_column='group',
        related_name='service_group',
        verbose_name="Grupo"
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        db_column='category',
        related_name='service_category',
        verbose_name="Categoría"
    )
    url = models.URLField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name="URL"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
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
        db_table = 'service'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['description']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # Actualizar updated_at automáticamente
        if not self._state.adding:  # Si no es una nueva instancia
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
