from django.contrib import admin
from .models import (
    BranchType, Branch, Platform, PlatformDetail,
    CompanyAgreement, Agreement, AgreementDetail
)


@admin.register(BranchType)
class BranchTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'type', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['type', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'type', 'description')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'branch', 'type', 'district', 'is_active', 'is_confirmed', 'created_at']
    list_filter = ['type', 'district', 'region', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['code', 'branch', 'description', 'address']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'branch', 'description')
        }),
        ('Ubicación', {
            'fields': ('type', 'district', 'region', 'address', 'maps_location')
        }),
        ('Contacto', {
            'fields': ('phone', 'mail', 'opening_hours')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'platform', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['platform', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'platform', 'description', 'website')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(PlatformDetail)
class PlatformDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'branch', 'platform', 'param_key', 'is_required', 'is_encrypted', 'is_active']
    list_filter = ['branch', 'platform', 'is_required', 'is_encrypted', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['code', 'param_key', 'param_value', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'branch', 'platform')
        }),
        ('Parámetros', {
            'fields': ('param_key', 'param_value', 'description')
        }),
        ('Configuración', {
            'fields': ('is_required', 'is_encrypted')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(CompanyAgreement)
class CompanyAgreementAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'company', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'created_at']
    search_fields = ['code', 'company', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'company', 'description')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'company', 'name', 'discount', 'start_date', 'end_date', 'is_active']
    list_filter = ['company', 'is_active', 'is_deleted', 'start_date', 'end_date', 'created_at']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'company', 'name', 'description')
        }),
        ('Detalles', {
            'fields': ('discount', 'start_date', 'end_date')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )


@admin.register(AgreementDetail)
class AgreementDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'company', 'agreement', 'branch', 'ticket', 'benefit_applied', 'is_active']
    list_filter = ['company', 'agreement', 'branch', 'ticket', 'benefit_applied', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'company', 'agreement', 'branch', 'ticket')
        }),
        ('Estado', {
            'fields': ('benefit_applied', 'is_active', 'is_deleted')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )








