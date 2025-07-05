from django.db import models
import uuid
from django.utils import timezone
from users.models import User

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
        if not self.is_confirmed:
            self.is_confirmed = False
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
        if not self.is_confirmed:
            self.is_confirmed = False
        super().save(*args, **kwargs)
