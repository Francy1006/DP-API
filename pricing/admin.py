from django.contrib import admin
from .models import (
    FiscalDirectiveType, FiscalDirective, FiscalFormula,
    PriceFiscalConfiguration, Price, FiscalConfigurationDetail
)

@admin.register(FiscalDirectiveType)
class FiscalDirectiveTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(FiscalDirective)
class FiscalDirectiveAdmin(admin.ModelAdmin):
    list_display = ['code', 'fiscal_directive', 'type', 'percentage', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['type', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'fiscal_directive', 'obs']
    ordering = ['fiscal_directive']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'fiscal_directive', 'type', 'percentage')
        }),
        ('Detalles', {
            'fields': ('obs', 'official_source_url')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FiscalFormula)
class FiscalFormulaAdmin(admin.ModelAdmin):
    list_display = ['id', 'formula', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['formula', 'formula_template']
    ordering = ['formula']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información de la Fórmula', {
            'fields': ('formula', 'formula_template')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PriceFiscalConfiguration)
class PriceFiscalConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'fiscal_configuration', 'fiscal_formula', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['fiscal_formula', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['fiscal_configuration']
    ordering = ['fiscal_configuration']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información de Configuración', {
            'fields': ('fiscal_configuration', 'fiscal_formula')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['code', 'net_amount', 'gross_amount', 'iva_amount', 'retention_amount', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información del Precio', {
            'fields': ('code', 'net_amount', 'gross_amount', 'iva_amount', 'retention_amount')
        }),
        ('Configuración Fiscal', {
            'fields': ('price_fiscal_configuration',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FiscalConfigurationDetail)
class FiscalConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'price_fiscal_configuration', 'price', 'fiscal_directive', 'log']
    list_filter = ['price_fiscal_configuration', 'price', 'fiscal_directive']
    search_fields = ['price_fiscal_configuration__fiscal_configuration', 'price__code', 'fiscal_directive__fiscal_directive']
    ordering = ['id']
    readonly_fields = ['id', 'log']
