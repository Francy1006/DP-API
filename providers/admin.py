from django.contrib import admin
from .models import (
    ProviderType, BankAccountType, Region, District, Bank, Provider
)

@admin.register(ProviderType)
class ProviderTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['region', 'description']
    search_fields = ['region', 'description']
    ordering = ['region']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['district', 'region', 'description']
    list_filter = ['region']
    search_fields = ['district', 'description', 'region__region']
    ordering = ['district']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank', 'description', 'created_at']
    search_fields = ['bank', 'description']
    ordering = ['bank']
    readonly_fields = ['created_at']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['code', 'provider', 'type', 'rating', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['type', 'rating', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'provider', 'contact_name', 'company_name']
    ordering = ['provider']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'provider', 'type', 'rating', 'obs_provider')
        }),
        ('Información de Contacto', {
            'fields': ('contact_name', 'contact_mail', 'contact_phone', 'contact_phone2', 'website_url', 'obs_contact')
        }),
        ('Información de la Empresa', {
            'fields': ('company_name', 'company_rut', 'company_activity', 'legal_representative')
        }),
        ('Información de Facturación', {
            'fields': ('billing_address', 'billing_mail', 'billing_phone')
        }),
        ('Información Bancaria', {
            'fields': ('company_bank', 'bank_account_type', 'bank_account_number', 'bank_account_mail')
        }),
        ('Información de Despacho', {
            'fields': ('dispatch_address', 'dispatch_maps_location', 'obs_dispatch', 'dispatch_district', 'dispatch_region')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )
