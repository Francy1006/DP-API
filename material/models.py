from django.db import models
from django.utils import timezone

from products.models import ItemCategory, ItemGroup, ItemType, Package
from users.models import User


_CODE_VERBOSE_NAME = "Código"
_CREATED_AT_VERBOSE_NAME = "Fecha de Creación"
_UPDATED_AT_VERBOSE_NAME = "Fecha de Actualización"
_CONFIRMED_AT_VERBOSE_NAME = "Fecha de Confirmación"
_DELETED_AT_VERBOSE_NAME = "Fecha de Eliminación"
_LOG_DEFAULT = "init;"
_VERSION_VERBOSE_NAME = "Versión"
_PACKAGE_UNIT_VERBOSE_NAME = "Unidad de Paquete"
_MIN_PACKAGE_PURCHASE_VERBOSE_NAME = "Compra Mínima de Paquete"


class Material(models.Model):
    """Unmanaged ORM mapping for the Flyway-owned Material table."""

    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36,
        unique=True,
        verbose_name=_CODE_VERBOSE_NAME,
    )
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name=_PACKAGE_UNIT_VERBOSE_NAME)
    min_package_purchase = models.IntegerField(
        verbose_name=_MIN_PACKAGE_PURCHASE_VERBOSE_NAME
    )
    # Kept scalar until Flyway repairs the three dangling legacy Price UUIDs.
    # New writes always link a real pricing.Price code through the use case.
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        db_column="provider",
        related_name="materials",
    )
    type = models.ForeignKey(
        ItemType,
        on_delete=models.PROTECT,
        db_column="type",
        related_name="materials",
    )
    item_group = models.ForeignKey(
        ItemGroup,
        on_delete=models.PROTECT,
        db_column="item_group",
        related_name="materials",
    )
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.PROTECT,
        db_column="category",
        related_name="materials",
    )
    url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="URL",
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        db_column="package",
        related_name="materials",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Eliminado",
    )
    is_confirmed = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Confirmado",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_CREATED_AT_VERBOSE_NAME,
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_UPDATED_AT_VERBOSE_NAME,
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_CONFIRMED_AT_VERBOSE_NAME,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_DELETED_AT_VERBOSE_NAME,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        to_field="code",
        related_name="materials_created",
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="confirmed_by",
        to_field="code",
        related_name="materials_confirmed",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="updated_by",
        to_field="code",
        related_name="materials_updated",
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="deleted_by",
        to_field="code",
        related_name="materials_deleted",
    )
    log = models.TextField(default=_LOG_DEFAULT, verbose_name="Log")
    version = models.IntegerField(
        default=1,
        verbose_name=_VERSION_VERBOSE_NAME,
    )

    class Meta:
        db_table = "material"
        managed = False
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description
