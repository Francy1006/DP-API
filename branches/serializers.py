from rest_framework import serializers
from .models import (
    BranchType, Branch, Platform, PlatformDetail,
    CompanyAgreement, Agreement, AgreementDetail
)
from django.db.models import Q


class BranchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchType
        fields = [
            'id', 'code', 'type', 'description', 'is_active',
            'created_at', 'updated_at', 'created_by', 'updated_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'log', 'version']


class BranchSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    district_name = serializers.CharField(source='district.district', read_only=True)
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = Branch
        fields = [
            'id', 'code', 'branch', 'description', 'type', 'type_name',
            'district', 'district_name', 'region', 'region_name',
            'address', 'maps_location', 'phone', 'mail', 'opening_hours',
            'is_active', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = [
            'id', 'code', 'platform', 'description', 'website', 'is_active',
            'created_at', 'updated_at', 'created_by', 'updated_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'log', 'version']


class PlatformDetailSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.branch', read_only=True)
    platform_name = serializers.CharField(source='platform.platform', read_only=True)
    
    class Meta:
        model = PlatformDetail
        fields = [
            'id', 'code', 'branch', 'branch_name', 'platform', 'platform_name',
            'param_key', 'param_value', 'description', 'is_required',
            'is_encrypted', 'is_active', 'is_deleted',
            'created_at', 'updated_at', 'deleted_at',
            'created_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']


class CompanyAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAgreement
        fields = [
            'id', 'code', 'company', 'description', 'is_active', 'is_deleted',
            'created_at', 'updated_at', 'deleted_at',
            'created_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']


class AgreementSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company', read_only=True)
    
    class Meta:
        model = Agreement
        fields = [
            'id', 'code', 'company', 'company_name', 'name', 'description',
            'discount', 'start_date', 'end_date', 'is_active', 'is_deleted',
            'created_at', 'updated_at', 'deleted_at',
            'created_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']


class AgreementDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company', read_only=True)
    agreement_name = serializers.CharField(source='agreement.name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch', read_only=True)
    ticket_description = serializers.CharField(source='ticket.description', read_only=True)
    
    class Meta:
        model = AgreementDetail
        fields = [
            'id', 'code', 'company', 'company_name', 'agreement', 'agreement_name',
            'branch', 'branch_name', 'ticket', 'ticket_description',
            'benefit_applied', 'is_active', 'is_deleted',
            'created_at', 'updated_at', 'deleted_at',
            'created_by', 'updated_by', 'deleted_by',
            'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'log', 'version']


class BranchWebSerializer(serializers.ModelSerializer):
    """
    Serializer específico para el endpoint web de branches
    Incluye todos los campos requeridos por la query SQL
    """
    region = serializers.CharField(source='region.region', read_only=True)
    district = serializers.CharField(source='district.district', read_only=True)
    # Campos de URLs de plataformas obtenidos desde PlatformDetail
    toteat_url = serializers.SerializerMethodField()
    uber_eats_url = serializers.SerializerMethodField()
    pedidos_ya_url = serializers.SerializerMethodField()
    whatsapp_channel_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = [
            'branch', 'tag', 'description', 'cover_image', 'secondary_image',
            'complementary_image', 'address', 'maps_location', 'region', 'district',
            'phone', 'opening_hours', 'toteat_url', 'uber_eats_url',
            'pedidos_ya_url', 'whatsapp_channel_url'
        ]
    
    def get_toteat_url(self, obj):
        """Obtiene la URL de Toteat desde PlatformDetail si existe"""
        try:
            platform_detail = PlatformDetail.objects.filter(
                branch=obj,
                platform__platform__icontains='toteat',
                is_active=True
            ).filter(
                Q(is_deleted=False) | Q(is_deleted__isnull=True)
            ).first()
            if platform_detail and platform_detail.param_key.lower() in ['url', 'link', 'toteat_url']:
                return platform_detail.param_value
        except:
            pass
        return None
    
    def get_uber_eats_url(self, obj):
        """Obtiene la URL de Uber Eats desde PlatformDetail si existe"""
        try:
            platform_detail = PlatformDetail.objects.filter(
                branch=obj,
                platform__platform__icontains='uber',
                is_active=True
            ).filter(
                Q(is_deleted=False) | Q(is_deleted__isnull=True)
            ).first()
            if platform_detail and platform_detail.param_key.lower() in ['url', 'link', 'uber_eats_url']:
                return platform_detail.param_value
        except:
            pass
        return None
    
    def get_pedidos_ya_url(self, obj):
        """Obtiene la URL de Pedidos Ya desde PlatformDetail si existe"""
        try:
            platform_detail = PlatformDetail.objects.filter(
                branch=obj,
                platform__platform__icontains='pedidos',
                is_active=True
            ).filter(
                Q(is_deleted=False) | Q(is_deleted__isnull=True)
            ).first()
            if platform_detail and platform_detail.param_key.lower() in ['url', 'link', 'pedidos_ya_url']:
                return platform_detail.param_value
        except:
            pass
        return None
    
    def get_whatsapp_channel_url(self, obj):
        """Obtiene la URL de WhatsApp Channel desde PlatformDetail si existe"""
        try:
            platform_detail = PlatformDetail.objects.filter(
                branch=obj,
                platform__platform__icontains='whatsapp',
                is_active=True
            ).filter(
                Q(is_deleted=False) | Q(is_deleted__isnull=True)
            ).first()
            if platform_detail and platform_detail.param_key.lower() in ['url', 'link', 'whatsapp_channel_url', 'whatsapp_url']:
                return platform_detail.param_value
        except:
            pass
        return None






