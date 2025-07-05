from django.db import models
from django.utils import timezone
from users.models import User

# Esta app está preparada para futuras implementaciones de ventas
# Por ahora se mantiene vacía pero con la estructura base

class SalesBase(models.Model):
    """
    Modelo base para entidades de ventas
    """
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='%(class)s_updated')

    class Meta:
        abstract = True
