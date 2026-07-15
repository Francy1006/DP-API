from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    FiscalDirectiveType, FiscalDirective, FiscalFormula, 
    PriceFiscalConfiguration, Price, FiscalConfigurationDetail
)
from .serializers import (
    FiscalDirectiveTypeSerializer, FiscalDirectiveSerializer, FiscalFormulaSerializer,
    PriceFiscalConfigurationSerializer, PriceSerializer, FiscalConfigurationDetailSerializer
)

# Create your views here.

class FiscalDirectiveTypeViewSet(viewsets.ModelViewSet):
    queryset = FiscalDirectiveType.objects.all()
    serializer_class = FiscalDirectiveTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']


class FiscalDirectiveViewSet(viewsets.ModelViewSet):
    queryset = FiscalDirective.objects.all()
    serializer_class = FiscalDirectiveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['fiscal_directive', 'obs']
    ordering_fields = ['fiscal_directive', 'created_at']
    ordering = ['fiscal_directive']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo directivas fiscales activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo directivas fiscales confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FiscalFormulaViewSet(viewsets.ModelViewSet):
    queryset = FiscalFormula.objects.all()
    serializer_class = FiscalFormulaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['formula', 'formula_template']
    ordering_fields = ['formula', 'created_at']
    ordering = ['formula']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo fórmulas fiscales activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo fórmulas fiscales confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PriceFiscalConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PriceFiscalConfiguration.objects.all()
    serializer_class = PriceFiscalConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fiscal_formula', 'is_deleted', 'is_confirmed']
    search_fields = ['fiscal_configuration']
    ordering_fields = ['fiscal_configuration', 'created_at']
    ordering = ['fiscal_configuration']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo configuraciones fiscales activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo configuraciones fiscales confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'price_configuration', 'price_record_type', 'is_current',
        'is_deleted', 'is_confirmed',
    ]
    search_fields = ['code', 'record_item_code']
    ordering_fields = [
        'code', 'base_net_amount', 'net_amount', 'gross_amount', 'created_at',
    ]
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Obtener solo precios vigentes"""
        queryset = self.get_queryset().filter(is_current=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo precios confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FiscalConfigurationDetailViewSet(viewsets.ModelViewSet):
    queryset = FiscalConfigurationDetail.objects.all()
    serializer_class = FiscalConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price_fiscal_configuration', 'price', 'fiscal_directive']
    search_fields = ['log']
    ordering_fields = ['id']
    ordering = ['id']
