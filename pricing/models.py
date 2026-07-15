from django.db import models
import uuid
from django.utils import timezone
from users.models import User


class FiscalDirectiveType(models.Model):
    """
    Modelo para tipos de directivas fiscales
    """

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = "fiscal_directive_type"
        verbose_name = "Tipo de Directiva Fiscal"
        verbose_name_plural = "Tipos de Directivas Fiscales"
        ordering = ["type"]

    def __str__(self):
        return self.type


class FiscalDirective(models.Model):
    """
    Modelo para directivas fiscales
    """

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    obs = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    fiscal_directive = models.CharField(
        max_length=50, unique=True, verbose_name="Directiva Fiscal"
    )
    type = models.ForeignKey(
        FiscalDirectiveType, on_delete=models.CASCADE, db_column="type"
    )
    percentage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Porcentaje"
    )
    official_source_url = models.CharField(
        max_length=255, verbose_name="URL de Fuente Oficial"
    )
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Eliminación"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        to_field="code",
        related_name="fiscal_directives_created",
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="confirmed_by",
        to_field="code",
        related_name="fiscal_directives_confirmed",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="updated_by",
        to_field="code",
        related_name="fiscal_directives_updated",
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="deleted_by",
        to_field="code",
        related_name="fiscal_directives_deleted",
    )

    class Meta:
        db_table = "fiscal_directive"
        verbose_name = "Directiva Fiscal"
        verbose_name_plural = "Directivas Fiscales"
        ordering = ["fiscal_directive"]

    def __str__(self):
        return self.fiscal_directive


class FiscalFormula(models.Model):
    """
    Modelo para fórmulas fiscales
    """

    id = models.CharField(
        primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID"
    )
    formula = models.CharField(max_length=50, verbose_name="Fórmula")
    formula_template = models.TextField(verbose_name="Plantilla de Fórmula")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Eliminación"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        to_field="code",
        related_name="fiscal_formulas_created",
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="confirmed_by",
        to_field="code",
        related_name="fiscal_formulas_confirmed",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="updated_by",
        to_field="code",
        related_name="fiscal_formulas_updated",
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="deleted_by",
        to_field="code",
        related_name="fiscal_formulas_deleted",
    )

    class Meta:
        db_table = "fiscal_formula"
        verbose_name = "Fórmula Fiscal"
        verbose_name_plural = "Fórmulas Fiscales"
        ordering = ["formula"]

    def __str__(self):
        return self.formula


class PriceFiscalConfiguration(models.Model):
    """
    Modelo para configuraciones fiscales de precios
    """

    id = models.CharField(
        primary_key=True, max_length=36, default=uuid.uuid4, verbose_name="ID"
    )
    fiscal_configuration = models.CharField(
        max_length=50, unique=True, verbose_name="Configuración Fiscal"
    )
    fiscal_formula = models.ForeignKey(
        FiscalFormula, on_delete=models.CASCADE, db_column="fiscal_formula"
    )
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Actualización"
    )
    confirmed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Confirmación"
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Eliminación"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="created_by",
        to_field="code",
        related_name="price_fiscal_configurations_created",
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="confirmed_by",
        to_field="code",
        related_name="price_fiscal_configurations_confirmed",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="updated_by",
        to_field="code",
        related_name="price_fiscal_configurations_updated",
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="deleted_by",
        to_field="code",
        related_name="price_fiscal_configurations_deleted",
    )

    class Meta:
        db_table = "price_fiscal_configuration"
        verbose_name = "Configuración Fiscal de Precio"
        verbose_name_plural = "Configuraciones Fiscales de Precios"
        ordering = ["fiscal_configuration"]

    def __str__(self):
        return self.fiscal_configuration


class Price(models.Model):
    id = models.AutoField(primary_key=True)

    code = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Código",
    )

    base_net_amount = models.IntegerField(
        default=0,
        verbose_name="Monto Neto Base",
    )

    net_amount = models.IntegerField(
        default=0,
        verbose_name="Monto Neto",
    )

    gross_amount = models.IntegerField(
        default=0,
        verbose_name="Monto Bruto",
    )

    iva_amount = models.IntegerField(
        default=0,
        verbose_name="Monto IVA",
    )

    aditional_tax_amount = models.IntegerField(
        default=0,
        verbose_name="Monto Impuesto Adicional",
    )

    retention_amount = models.IntegerField(
        default=0,
        verbose_name="Monto de Retención",
    )

    price_configuration = models.CharField(
        max_length=36,
        db_column="price_configuration",
        verbose_name="Configuración de Precio",
    )

    is_current = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name="Precio Vigente",
    )

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
        null=True,
        blank=True,
        verbose_name="Fecha de Creación",
    )

    created_by = models.ForeignKey(
        User,
        db_column="created_by",
        to_field="code",
        on_delete=models.PROTECT,
        related_name="prices_created",
        verbose_name="Creado por",
    )

    record_item_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Código del Registro",
    )

    price_record_type = models.IntegerField(
        db_column="price_record_type",
        null=True,
        blank=True,
        verbose_name="Tipo de Registro de Precio",
    )

    class Meta:
        db_table = "price"
        managed = False
        verbose_name = "Precio"
        verbose_name_plural = "Precios"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - ${self.gross_amount}"


class FiscalConfigurationDetail(models.Model):
    """
    Modelo para detalles de configuración fiscal
    """

    id = models.AutoField(primary_key=True)
    price_fiscal_configuration = models.ForeignKey(
        PriceFiscalConfiguration,
        on_delete=models.CASCADE,
        db_column="price_fiscal_configuration",
    )
    price = models.ForeignKey(
        Price, on_delete=models.CASCADE, db_column="price", to_field="code"
    )
    fiscal_directive = models.ForeignKey(
        FiscalDirective,
        on_delete=models.CASCADE,
        db_column="fiscal_directive",
        to_field="code",
    )
    log = models.TextField(default="init;", verbose_name="Log")

    class Meta:
        db_table = "fiscal_configuration_detail"
        verbose_name = "Detalle de Configuración Fiscal"
        verbose_name_plural = "Detalles de Configuración Fiscal"
        unique_together = ["id", "price", "fiscal_directive"]

    def __str__(self):
        return f"{self.price_fiscal_configuration} - {self.price} - {self.fiscal_directive}"
