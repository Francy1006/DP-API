from django.contrib import admin
from .models import ItemFilterClassification


@admin.register(ItemFilterClassification)
class ItemFilterClassificationAdmin(admin.ModelAdmin):
    list_display = ['classification', 'description']
    search_fields = ['classification', 'description']
    ordering = ['classification']


