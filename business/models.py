from django.db import models


class ItemFilterClassification(models.Model):
    """
    Modelo para clasificación de filtros de items
    """
    id = models.AutoField(primary_key=True)
    classification = models.CharField(max_length=50, verbose_name="Clasificación")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'item_filter_classification'
        verbose_name = "Clasificación de Filtro de Items"
        verbose_name_plural = "Clasificaciones de Filtro de Items"
        ordering = ['classification']

    def __str__(self):
        return self.classification



