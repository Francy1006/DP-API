from django.contrib import admin
from .models import ItemGroup


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ItemGroup
    """
    list_display = ['id', 'group_name', 'description', 'cataloge_render']
    list_filter = ['cataloge_render']
    search_fields = ['group_name', 'description']
    list_editable = ['cataloge_render']
    readonly_fields = ['id']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('group_name', 'description')
        }),
        ('Configuración', {
            'fields': ('cataloge_render',)
        }),
        ('Información del Sistema', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 20
    ordering = ['group_name']
    
    def get_queryset(self, request):
        """
        Optimizar consultas con select_related si hay relaciones
        """
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        """
        Personalizar el guardado del modelo
        """
        super().save_model(request, obj, form, change)
