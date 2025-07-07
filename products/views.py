from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Menu, ItemCategory, ItemType, ItemGroup, PackageType, TransportType,
    MeasureUnit, Package, Catalog, ItemConfiguration, ItemConfigurationDetail,
    Product, Material, Service
)
from .serializers import (
    MenuSerializer, ItemCategorySerializer, ItemTypeSerializer, ItemGroupSerializer,
    PackageTypeSerializer, TransportTypeSerializer, MeasureUnitSerializer,
    PackageSerializer, CatalogSerializer, ItemConfigurationSerializer,
    ItemConfigurationDetailSerializer, ProductSerializer, MaterialSerializer, ServiceSerializer
)

# Create your views here.

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['menu']
    search_fields = ['menu', 'description']
    ordering_fields = ['menu', 'description']
    ordering = ['menu']




class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'catalog_render']
    search_fields = ['category', 'description']
    ordering_fields = ['category', 'description']
    ordering = ['category']

    @action(detail=False, methods=['get'])
    def catalog_categories(self, request):
        """Obtener solo categorías que se renderizan en catálogo"""
        catalog_categories = self.queryset.filter(catalog_render=True)
        serializer = self.get_serializer(catalog_categories, many=True)
        return Response(serializer.data)


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'description']
    ordering = ['type']


class ItemGroupViewSet(viewsets.ModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group_name', 'catalog_render']
    search_fields = ['group_name', 'description']
    ordering_fields = ['group_name', 'description']
    ordering = ['group_name']

    @action(detail=False, methods=['get'])
    def catalog_groups(self, request):
        """Obtener solo grupos que se renderizan en catálogo"""
        catalog_groups = self.queryset.filter(catalog_render=True)
        serializer = self.get_serializer(catalog_groups, many=True)
        return Response(serializer.data)


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'description']
    ordering = ['type']


class TransportTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportType.objects.all()
    serializer_class = TransportTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'description']
    ordering = ['type']


class MeasureUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['measure_unit']
    search_fields = ['measure_unit', 'description']
    ordering_fields = ['measure_unit', 'description']
    ordering = ['measure_unit']


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['package_type', 'transport_type', 'is_deleted', 'is_confirmed']
    search_fields = ['description']
    ordering_fields = ['description', 'created_at']
    ordering = ['description']


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['menu', 'group', 'category', 'type', 'chef_recommendation', 'is_visible', 'is_deleted', 'is_confirmed']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'sku', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def visible(self, request):
        """Obtener solo catálogos visibles"""
        visible_catalogs = self.queryset.filter(is_visible=True)
        serializer = self.get_serializer(visible_catalogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def chef_recommendations(self, request):
        """Obtener solo catálogos recomendados por el chef"""
        chef_recommendations = self.queryset.filter(
            chef_recommendation=True, 
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True
        )
        serializer = self.get_serializer(chef_recommendations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def salsas(self, request):
        """Obtener solo catálogos de salsas"""
        salsas = self.queryset.filter(
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True,
            category_id=2  # ID de la categoría "salsa"
        )
        serializer = self.get_serializer(salsas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pastas(self, request):
        """Obtener solo catálogos de pastas"""
        pastas = self.queryset.filter(
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True,
            category_id=1  # ID de la categoría "pasta"
        )
        serializer = self.get_serializer(pastas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def franchise_only_catalogs(self, request):
        """Obtener catálogos confirmados, activos, no eliminados y solo de franquicia"""
        franchise_only_catalogs = self.queryset.filter(
            is_confirmed=True,
            is_visible=True,  # equivalente a is_active para catálogos
            is_deleted__isnull=True,
            menu__franchise_only=True
        )
        serializer = self.get_serializer(franchise_only_catalogs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_visibility(self, request, pk=None):
        """Alternar visibilidad del catálogo"""
        catalog = self.get_object()
        catalog.is_visible = not catalog.is_visible
        catalog.save()
        serializer = self.get_serializer(catalog)
        return Response(serializer.data)


class ItemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = ItemConfiguration.objects.all()
    serializer_class = ItemConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['package', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'configuration', 'description']
    ordering_fields = ['configuration', 'created_at']
    ordering = ['configuration']


class ItemConfigurationDetailViewSet(viewsets.ModelViewSet):
    queryset = ItemConfigurationDetail.objects.all()
    serializer_class = ItemConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'configuration', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'detail', 'id_item']
    ordering_fields = ['code', 'detail']
    ordering = ['code']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'sku', 'description']
    ordering_fields = ['description', 'created_at']
    ordering = ['description']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo productos activos"""
        active_products = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_products, many=True)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'sku', 'description']
    ordering_fields = ['description', 'created_at']
    ordering = ['description']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo materiales activos"""
        active_materials = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_materials, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'sku', 'description']
    ordering_fields = ['description', 'created_at']
    ordering = ['description']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo servicios activos"""
        active_services = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_services, many=True)
        return Response(serializer.data)
