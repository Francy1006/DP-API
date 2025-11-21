from django.db import models
import uuid
from django.utils import timezone
from users.models import User


class Ticket(models.Model):
    """
    Modelo para tickets
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    cover_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Complementaria")
    image_gallery = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Galería de Imágenes")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Paquete")
    min_package_purchase = models.IntegerField(default=1, verbose_name="Compra Mínima de Paquete")
    price = models.CharField(max_length=36, verbose_name="Precio")
    type = models.ForeignKey('products.ItemType', on_delete=models.CASCADE, db_column='type')
    item_group = models.ForeignKey('products.ItemGroup', on_delete=models.CASCADE, db_column='item_group')
    category = models.ForeignKey('products.ItemCategory', on_delete=models.CASCADE, db_column='category')
    filter_classification = models.ForeignKey('business.ItemFilterClassification', on_delete=models.CASCADE, db_column='filter_classification', verbose_name="Clasificación de Filtro")
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL")
    package = models.ForeignKey('products.Package', on_delete=models.CASCADE, db_column='package')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='tickets_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='tickets_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='tickets_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='tickets_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")

    class Meta:
        db_table = 'ticket'
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.is_confirmed:
            self.is_confirmed = False
        super().save(*args, **kwargs)






