from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import (
    ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, Catalog, Provider,
    PackageType, TransportType, MeasureUnit, ProviderType, BankAccountType, Region, District,
    Bank, UserType, User, UserToken, Package
)
from .serializers import (
    ItemGroupSerializer, ItemGroupListSerializer,
    MenuSerializer, MenuListSerializer,
    ItemCategorySerializer, ItemCategoryListSerializer,
    ItemTypeSerializer, ItemTypeListSerializer,
    InstructionTypeSerializer, InstructionTypeListSerializer,
    InstructionSerializer, InstructionListSerializer,
    InstructionCreateSerializer, InstructionUpdateSerializer,
    CatalogSerializer, CatalogListSerializer, CatalogCreateSerializer, CatalogUpdateSerializer,
    ProviderSerializer, ProviderListSerializer, ProviderCreateSerializer, ProviderUpdateSerializer,
    PackageTypeSerializer, PackageTypeListSerializer,
    TransportTypeSerializer, TransportTypeListSerializer,
    MeasureUnitSerializer, MeasureUnitListSerializer,
    ProviderTypeSerializer, ProviderTypeListSerializer,
    BankAccountTypeSerializer, BankAccountTypeListSerializer,
    RegionSerializer, RegionListSerializer,
    DistrictSerializer, DistrictListSerializer,
    BankSerializer, BankListSerializer,
    UserTypeSerializer, UserTypeListSerializer,
    UserSerializer, UserListSerializer,
    UserTokenSerializer, UserTokenListSerializer,
    PackageSerializer, PackageListSerializer
)


# Menu ViewSet
class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Menu
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['menu', 'description']
    ordering_fields = ['menu']
    ordering = ['menu']

    def get_serializer_class(self):
        if self.action == 'list':
            return MenuListSerializer
        return MenuSerializer


# ItemCategory ViewSet
class ItemCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemCategory
    """
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['catalog_render']
    search_fields = ['category', 'description']
    ordering_fields = ['category']
    ordering = ['category']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemCategoryListSerializer
        return ItemCategorySerializer

    @action(detail=False, methods=['get'])
    def catalog_categories(self, request):
        """
        Endpoint para obtener solo categorías que se renderizan en catálogo
        """
        queryset = self.queryset.filter(catalog_render=True)
        serializer = ItemCategoryListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_catalog_render(self, request, pk=None):
        """
        Endpoint para alternar el estado de renderizado en catálogo
        """
        item_category = self.get_object()
        item_category.catalog_render = not item_category.catalog_render
        item_category.save()
        serializer = self.get_serializer(item_category)
        return Response(serializer.data)


# ItemType ViewSet
class ItemTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemType
    """
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemTypeListSerializer
        return ItemTypeSerializer


# ItemGroup ViewSet
class ItemGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemGroup
    """
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering_fields = ['group_name']
    ordering = ['group_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemGroupListSerializer
        return ItemGroupSerializer

    @action(detail=False, methods=['get'])
    def catalog_groups(self, request):
        """
        Endpoint para obtener solo grupos que se renderizan en catálogo
        """
        queryset = self.queryset.filter(catalog_render=True)
        serializer = ItemGroupListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_catalog_render(self, request, pk=None):
        """
        Endpoint para alternar el estado de renderizado en catálogo
        """
        item_group = self.get_object()
        item_group.catalog_render = not item_group.catalog_render
        item_group.save()
        serializer = self.get_serializer(item_group)
        return Response(serializer.data)


# PackageType ViewSet
class PackageTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de PackageType
    """
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return PackageTypeListSerializer
        return PackageTypeSerializer


# TransportType ViewSet
class TransportTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de TransportType
    """
    queryset = TransportType.objects.all()
    serializer_class = TransportTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return TransportTypeListSerializer
        return TransportTypeSerializer


# MeasureUnit ViewSet
class MeasureUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de MeasureUnit
    """
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['measure_unit', 'description']
    ordering_fields = ['measure_unit']
    ordering = ['measure_unit']

    def get_serializer_class(self):
        if self.action == 'list':
            return MeasureUnitListSerializer
        return MeasureUnitSerializer


# ProviderType ViewSet
class ProviderTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ProviderType
    """
    queryset = ProviderType.objects.all()
    serializer_class = ProviderTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProviderTypeListSerializer
        return ProviderTypeSerializer


# BankAccountType ViewSet
class BankAccountTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de BankAccountType
    """
    queryset = BankAccountType.objects.all()
    serializer_class = BankAccountTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return BankAccountTypeListSerializer
        return BankAccountTypeSerializer


# Region ViewSet
class RegionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Region
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['region', 'description']
    ordering_fields = ['region']
    ordering = ['region']

    def get_serializer_class(self):
        if self.action == 'list':
            return RegionListSerializer
        return RegionSerializer


# District ViewSet
class DistrictViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de District
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region']
    search_fields = ['district', 'description']
    ordering_fields = ['district']
    ordering = ['district']

    def get_serializer_class(self):
        if self.action == 'list':
            return DistrictListSerializer
        return DistrictSerializer


# Bank ViewSet
class BankViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Bank
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bank', 'description']
    ordering_fields = ['bank']
    ordering = ['bank']

    def get_serializer_class(self):
        if self.action == 'list':
            return BankListSerializer
        return BankSerializer


# UserType ViewSet
class UserTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de UserType
    """
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserTypeListSerializer
        return UserTypeSerializer


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['name', 'last_name', 'mail', 'google_id']
    ordering_fields = ['name', 'last_name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Filtrar usuarios eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# UserToken ViewSet
class UserTokenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de UserToken
    """
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id', 'revoked_at']
    search_fields = ['ip_address', 'user_agent']
    ordering_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserTokenListSerializer
        return UserTokenSerializer


# InstructionType ViewSet
class InstructionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de InstructionType
    """
    queryset = InstructionType.objects.all()
    serializer_class = InstructionTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return InstructionTypeListSerializer
        return InstructionTypeSerializer

    def get_queryset(self):
        """
        Filtrar tipos de instrucción eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# Instruction ViewSet
class InstructionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Instruction
    """
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['instruction', 'description']
    ordering_fields = ['instruction', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return InstructionListSerializer
        elif self.action == 'create':
            return InstructionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InstructionUpdateSerializer
        return InstructionSerializer

    def get_queryset(self):
        """
        Filtrar instrucciones eliminadas por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo instrucciones activas (no eliminadas)
        """
        queryset = self.queryset.filter(is_deleted__isnull=True)
        serializer = InstructionListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """
        Endpoint para obtener solo instrucciones confirmadas
        """
        queryset = self.queryset.filter(is_confirmed=True)
        serializer = InstructionListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Endpoint para confirmar una instrucción
        """
        instruction = self.get_object()
        instruction.is_confirmed = True
        instruction.confirmed_at = timezone.now()
        instruction.confirmed_by = request.data.get('confirmed_by')
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """
        Endpoint para eliminación lógica de una instrucción
        """
        instruction = self.get_object()
        instruction.is_deleted = True
        instruction.deleted_at = timezone.now()
        instruction.deleted_by = request.data.get('deleted_by')
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Endpoint para restaurar una instrucción eliminada
        """
        instruction = self.get_object()
        instruction.is_deleted = False
        instruction.deleted_at = None
        instruction.deleted_by = None
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)


# Package ViewSet
class PackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Package
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['package_type', 'transport_type', 'measure_unit', 'is_deleted', 'is_confirmed']
    search_fields = ['description']
    ordering_fields = ['description', 'created_at']
    ordering = ['description']

    def get_serializer_class(self):
        if self.action == 'list':
            return PackageListSerializer
        return PackageSerializer

    def get_queryset(self):
        """
        Filtrar paquetes eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# Catalog ViewSet
class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Catalog
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['menu', 'group', 'category', 'type', 'chef_recommendation', 'is_visible', 'is_deleted', 'is_confirmed']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogListSerializer
        elif self.action == 'create':
            return CatalogCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CatalogUpdateSerializer
        return CatalogSerializer

    def get_queryset(self):
        """
        Filtrar catálogos eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def visible(self, request):
        """
        Endpoint para obtener solo catálogos visibles
        """
        queryset = self.queryset.filter(is_visible=True, is_deleted__isnull=True)
        serializer = CatalogListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_visibility(self, request, pk=None):
        """
        Endpoint para alternar la visibilidad de un catálogo
        """
        catalog = self.get_object()
        catalog.is_visible = not catalog.is_visible
        catalog.save()
        serializer = self.get_serializer(catalog)
        return Response(serializer.data)


# Provider ViewSet
class ProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Provider
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_deleted', 'is_confirmed', 'dispatch_region', 'dispatch_district']
    search_fields = ['provider', 'contact_name', 'company_name', 'contact_mail']
    ordering_fields = ['provider', 'rating', 'created_at']
    ordering = ['provider']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProviderListSerializer
        elif self.action == 'create':
            return ProviderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProviderUpdateSerializer
        return ProviderSerializer

    def get_queryset(self):
        """
        Filtrar proveedores eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo proveedores activos
        """
        queryset = self.queryset.filter(is_active=True, is_deleted__isnull=True)
        serializer = ProviderListSerializer(queryset, many=True)
        return Response(serializer.data)
