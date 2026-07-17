from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ProviderType, ProviderGroup, Region, District, Bank, BankAccountType
from .serializers import (
    ProviderTypeSerializer, ProviderGroupSerializer,
    RegionSerializer, DistrictSerializer, BankSerializer, BankAccountTypeSerializer
)
from .presentation.views import ProviderViewSet

# Create your views here.

class ProviderTypeViewSet(viewsets.ModelViewSet):
    queryset = ProviderType.objects.all()
    serializer_class = ProviderTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']


class ProviderGroupViewSet(viewsets.ModelViewSet):
    queryset = ProviderGroup.objects.all()
    serializer_class = ProviderGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['group_name', 'description']
    ordering_fields = ['group_name']
    ordering = ['group_name']

    @action(detail=False, methods=['get'])
    def catalog_groups(self, request):
        """Obtener solo grupos que se renderizan en catálogo"""
        queryset = self.get_queryset().filter(catalog_render=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['region', 'description']
    ordering_fields = ['region']
    ordering = ['region']


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region']
    search_fields = ['district', 'description']
    ordering_fields = ['district']
    ordering = ['district']


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bank', 'description']
    ordering_fields = ['bank']
    ordering = ['bank']


class BankAccountTypeViewSet(viewsets.ModelViewSet):
    queryset = BankAccountType.objects.all()
    serializer_class = BankAccountTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']
