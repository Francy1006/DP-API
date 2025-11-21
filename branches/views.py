from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    BranchType, Branch, Platform, PlatformDetail,
    CompanyAgreement, Agreement, AgreementDetail
)
from .serializers import (
    BranchTypeSerializer, BranchSerializer, BranchWebSerializer, PlatformSerializer, PlatformDetailSerializer,
    CompanyAgreementSerializer, AgreementSerializer, AgreementDetailSerializer
)


class BranchTypeViewSet(viewsets.ModelViewSet):
    queryset = BranchType.objects.all()
    serializer_class = BranchTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'created_at']
    ordering = ['type']


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'district', 'region', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'branch', 'description', 'address']
    ordering_fields = ['branch', 'created_at']
    ordering = ['branch']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo sucursales activas"""
        active_branches = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_branches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def web(self, request):
        """
        Endpoint para obtener sucursales para el sitio web
        Filtra: branch != 'FRANQUICIA', is_active=True, is_confirmed=True, (is_deleted=False or is_deleted=None)
        Ordena por id ASC
        """
        from django.db.models import Q
        
        # Aplicar los filtros según la query SQL
        queryset = Branch.objects.select_related('region', 'district').filter(
            ~Q(branch='FRANQUICIA'),
            is_active=True,
            is_confirmed=True
        ).filter(
            Q(is_deleted=False) | Q(is_deleted__isnull=True)
        ).order_by('id')
        
        serializer = BranchWebSerializer(queryset, many=True)
        return Response(serializer.data)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['platform', 'description']
    ordering_fields = ['platform', 'created_at']
    ordering = ['platform']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo plataformas activas"""
        active_platforms = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_platforms, many=True)
        return Response(serializer.data)


class PlatformDetailViewSet(viewsets.ModelViewSet):
    queryset = PlatformDetail.objects.all()
    serializer_class = PlatformDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['branch', 'platform', 'is_required', 'is_encrypted', 'is_active', 'is_deleted']
    search_fields = ['code', 'param_key', 'param_value', 'description']
    ordering_fields = ['branch', 'platform', 'param_key']
    ordering = ['branch', 'platform']


class CompanyAgreementViewSet(viewsets.ModelViewSet):
    queryset = CompanyAgreement.objects.all()
    serializer_class = CompanyAgreementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted']
    search_fields = ['code', 'company', 'description']
    ordering_fields = ['company', 'created_at']
    ordering = ['company']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo empresas activas"""
        active_companies = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_companies, many=True)
        return Response(serializer.data)


class AgreementViewSet(viewsets.ModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'is_active', 'is_deleted']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['name', 'start_date', 'created_at']
    ordering = ['company', 'name']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo convenios activos"""
        active_agreements = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_agreements, many=True)
        return Response(serializer.data)


class AgreementDetailViewSet(viewsets.ModelViewSet):
    queryset = AgreementDetail.objects.all()
    serializer_class = AgreementDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'agreement', 'branch', 'ticket', 'benefit_applied', 'is_active', 'is_deleted']
    search_fields = ['code']
    ordering_fields = ['company', 'agreement', 'branch']
    ordering = ['company', 'agreement', 'branch']






