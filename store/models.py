from django.db import models

# Create your models here.

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        db_table = 'item_group'
        verbose_name = "Grupo de Items"
        verbose_name_plural = "Grupos de Items"
        ordering = ['group_name']

    def __str__(self):
        return self.group_name
