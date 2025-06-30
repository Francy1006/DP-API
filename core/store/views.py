from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import (
    ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction,
    Catalog, Restriction, PermissionType, Permission, Role, RestrictionRoles, 
    RolePermissions, PackageType, TransportType, MeasureUnit, ProviderType,
    BankAccountType, Region, District, Bank, UserType, User, UserToken, 
    Package, ItemConfiguration, ItemConfigurationDetail, Provider, Product, 
    Material, Service
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
    RestrictionSerializer, RestrictionListSerializer, RestrictionCreateSerializer, RestrictionUpdateSerializer,
    PermissionTypeSerializer, PermissionTypeListSerializer,
    PermissionSerializer, PermissionListSerializer,
    RoleSerializer, RoleListSerializer,
    RestrictionRolesSerializer, RestrictionRolesListSerializer,
    RolePermissionsSerializer, RolePermissionsListSerializer,
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
    PackageSerializer, PackageListSerializer,
    ItemConfigurationSerializer, ItemConfigurationListSerializer,
    ItemConfigurationDetailSerializer, ItemConfigurationDetailListSerializer,
    ProviderSerializer, ProviderListSerializer,
    ProductSerializer, ProductListSerializer,
    MaterialSerializer, MaterialListSerializer,
    ServiceSerializer, ServiceListSerializer
)


# Menu ViewSet
class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Menu
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type']
    ordering = ['type']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemTypeListSerializer
        return ItemTypeSerializer


# ItemGroup ViewSet (existing)
class ItemGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemGroup
    """
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering_fields = ['group_name']
    ordering = ['group_name']

    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción
        """
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


# InstructionType ViewSet
class InstructionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de InstructionType
    """
    queryset = InstructionType.objects.all()
    serializer_class = InstructionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return InstructionTypeListSerializer
        return InstructionTypeSerializer


# Instruction ViewSet
class InstructionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Instruction
    """
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
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
        # Por defecto, no mostrar instrucciones eliminadas
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
        queryset = self.queryset.filter(is_confirmed=True, is_deleted__isnull=True)
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
        instruction.confirmed_by = request.data.get('confirmed_by', 'system')
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
        instruction.deleted_by = request.data.get('deleted_by', 'system')
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


# API Views individuales para mayor control
from rest_framework.views import APIView


# Menu API Views
class MenuListAPIView(APIView):
    """
    Vista para listar y crear menús
    """

    def get(self, request):
        queryset = Menu.objects.all()
        serializer = MenuListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar un menú específico
    """

    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return None

    def get(self, request, pk):
        menu = self.get_object(pk)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk):
        menu = self.get_object(pk)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = self.get_object(pk)
        if menu is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ItemCategory API Views
class ItemCategoryListAPIView(APIView):
    """
    Vista para listar y crear categorías de items
    """

    def get(self, request):
        queryset = ItemCategory.objects.all()
        serializer = ItemCategoryListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemCategoryDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar una categoría específica
    """

    def get_object(self, pk):
        try:
            return ItemCategory.objects.get(pk=pk)
        except ItemCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        item_category = self.get_object(pk)
        if item_category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemCategorySerializer(item_category)
        return Response(serializer.data)

    def put(self, request, pk):
        item_category = self.get_object(pk)
        if item_category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemCategorySerializer(item_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item_category = self.get_object(pk)
        if item_category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ItemType API Views
class ItemTypeListAPIView(APIView):
    """
    Vista para listar y crear tipos de items
    """

    def get(self, request):
        queryset = ItemType.objects.all()
        serializer = ItemTypeListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemTypeDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar un tipo específico
    """

    def get_object(self, pk):
        try:
            return ItemType.objects.get(pk=pk)
        except ItemType.DoesNotExist:
            return None

    def get(self, request, pk):
        item_type = self.get_object(pk)
        if item_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemTypeSerializer(item_type)
        return Response(serializer.data)

    def put(self, request, pk):
        item_type = self.get_object(pk)
        if item_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemTypeSerializer(item_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item_type = self.get_object(pk)
        if item_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# InstructionType API Views
class InstructionTypeListAPIView(APIView):
    """
    Vista para listar y crear tipos de instrucciones
    """

    def get(self, request):
        queryset = InstructionType.objects.all()
        serializer = InstructionTypeListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstructionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructionTypeDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar un tipo de instrucción específico
    """

    def get_object(self, pk):
        try:
            return InstructionType.objects.get(pk=pk)
        except InstructionType.DoesNotExist:
            return None

    def get(self, request, pk):
        instruction_type = self.get_object(pk)
        if instruction_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InstructionTypeSerializer(instruction_type)
        return Response(serializer.data)

    def put(self, request, pk):
        instruction_type = self.get_object(pk)
        if instruction_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InstructionTypeSerializer(instruction_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instruction_type = self.get_object(pk)
        if instruction_type is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instruction_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Instruction API Views
class InstructionListAPIView(APIView):
    """
    Vista para listar y crear instrucciones
    """

    def get(self, request):
        queryset = Instruction.objects.filter(is_deleted__isnull=True)
        serializer = InstructionListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstructionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructionDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar una instrucción específica
    """

    def get_object(self, pk):
        try:
            return Instruction.objects.get(pk=pk)
        except Instruction.DoesNotExist:
            return None

    def get(self, request, pk):
        instruction = self.get_object(pk)
        if instruction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InstructionSerializer(instruction)
        return Response(serializer.data)

    def put(self, request, pk):
        instruction = self.get_object(pk)
        if instruction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InstructionUpdateSerializer(instruction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instruction = self.get_object(pk)
        if instruction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Eliminación lógica
        instruction.is_deleted = True
        instruction.deleted_at = timezone.now()
        instruction.deleted_by = request.data.get('deleted_by', 'system')
        instruction.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ItemGroup API Views (existing)
class ItemGroupListAPIView(APIView):
    """
    Vista para listar y crear grupos de items
    """

    def get(self, request):
        """
        Listar todos los grupos de items
        """
        queryset = ItemGroup.objects.all()
        serializer = ItemGroupListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Crear un nuevo grupo de items
        """
        serializer = ItemGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemGroupDetailAPIView(APIView):
    """
    Vista para obtener, actualizar y eliminar un grupo de items específico
    """

    def get_object(self, pk):
        try:
            return ItemGroup.objects.get(pk=pk)
        except ItemGroup.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Obtener un grupo de items específico
        """
        item_group = self.get_object(pk)
        if item_group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemGroupSerializer(item_group)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Actualizar un grupo de items
        """
        item_group = self.get_object(pk)
        if item_group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemGroupSerializer(item_group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Eliminar un grupo de items
        """
        item_group = self.get_object(pk)
        if item_group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Catalog ViewSet
class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Catalog
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['menu', 'group', 'category', 'type', 'is_visible', 'is_deleted', 'is_confirmed']
    search_fields = ['sku', 'name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
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


# Restriction ViewSet
class RestrictionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Restriction
    """
    queryset = Restriction.objects.all()
    serializer_class = RestrictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['restriction', 'description']
    ordering_fields = ['restriction', 'created_at']
    ordering = ['restriction']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestrictionListSerializer
        elif self.action == 'create':
            return RestrictionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RestrictionUpdateSerializer
        return RestrictionSerializer

    def get_queryset(self):
        """
        Filtrar restricciones eliminadas por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# PermissionType ViewSet
class PermissionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de PermissionType
    """
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PermissionTypeListSerializer
        return PermissionTypeSerializer


# Permission ViewSet
class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Permission
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['permission', 'description']
    ordering_fields = ['permission', 'created_at']
    ordering = ['permission']

    def get_serializer_class(self):
        if self.action == 'list':
            return PermissionListSerializer
        return PermissionSerializer

    def get_queryset(self):
        """
        Filtrar permisos eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# Role ViewSet
class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Role
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['role', 'description']
    ordering_fields = ['role', 'created_at']
    ordering = ['role']

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer

    def get_queryset(self):
        """
        Filtrar roles eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# RestrictionRoles ViewSet
class RestrictionRolesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de RestrictionRoles
    """
    queryset = RestrictionRoles.objects.all()
    serializer_class = RestrictionRolesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restriction', 'role', 'is_deleted', 'is_confirmed']
    ordering_fields = ['restriction', 'role', 'created_at']
    ordering = ['restriction', 'role']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestrictionRolesListSerializer
        return RestrictionRolesSerializer

    def get_queryset(self):
        """
        Filtrar relaciones eliminadas por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# RolePermissions ViewSet
class RolePermissionsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de RolePermissions
    """
    queryset = RolePermissions.objects.all()
    serializer_class = RolePermissionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'permission', 'is_deleted', 'is_confirmed']
    ordering_fields = ['role', 'permission', 'created_at']
    ordering = ['role', 'permission']

    def get_serializer_class(self):
        if self.action == 'list':
            return RolePermissionsListSerializer
        return RolePermissionsSerializer

    def get_queryset(self):
        """
        Filtrar relaciones eliminadas por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# PackageType ViewSet
class PackageTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de PackageType
    """
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region']
    search_fields = ['district', 'description']
    ordering_fields = ['district', 'region']
    ordering = ['region', 'district']

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bank', 'description']
    ordering_fields = ['bank', 'created_at']
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'created_at']
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['name', 'last_name', 'mail', 'google_id']
    ordering_fields = ['name', 'last_name', 'created_at']
    ordering = ['name', 'last_name']

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

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo usuarios activos
        """
        queryset = self.queryset.filter(is_active=True, is_deleted__isnull=True)
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


# UserToken ViewSet
class UserTokenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de UserToken
    """
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id']
    search_fields = ['ip_address']
    ordering_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserTokenListSerializer
        return UserTokenSerializer


# Package ViewSet
class PackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Package
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
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


# ItemConfiguration ViewSet
class ItemConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemConfiguration
    """
    queryset = ItemConfiguration.objects.all()
    serializer_class = ItemConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['package', 'is_deleted', 'is_confirmed']
    search_fields = ['configuration', 'description']
    ordering_fields = ['configuration', 'created_at']
    ordering = ['configuration']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemConfigurationListSerializer
        return ItemConfigurationSerializer

    def get_queryset(self):
        """
        Filtrar configuraciones eliminadas por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# ItemConfigurationDetail ViewSet
class ItemConfigurationDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemConfigurationDetail
    """
    queryset = ItemConfigurationDetail.objects.all()
    serializer_class = ItemConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'configuration', 'is_deleted', 'is_confirmed']
    search_fields = ['detail', 'id_item']
    ordering_fields = ['configuration', 'detail', 'created_at']
    ordering = ['configuration', 'detail']

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemConfigurationDetailListSerializer
        return ItemConfigurationDetailSerializer

    def get_queryset(self):
        """
        Filtrar detalles eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset


# Provider ViewSet
class ProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Provider
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_deleted', 'is_confirmed', 'dispatch_region', 'dispatch_district']
    search_fields = ['provider', 'contact_name', 'company_name', 'contact_mail']
    ordering_fields = ['provider', 'rating', 'created_at']
    ordering = ['provider']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProviderListSerializer
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


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'package', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['sku', 'description', 'OBS']
    ordering_fields = ['description', 'gross_price', 'created_at']
    ordering = ['description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        """
        Filtrar productos eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo productos activos
        """
        queryset = self.queryset.filter(is_active=True, is_deleted__isnull=True)
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)


# Material ViewSet
class MaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Material
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'package', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['sku', 'description', 'OBS']
    ordering_fields = ['description', 'gross_price', 'created_at']
    ordering = ['description']

    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialListSerializer
        return MaterialSerializer

    def get_queryset(self):
        """
        Filtrar materiales eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo materiales activos
        """
        queryset = self.queryset.filter(is_active=True, is_deleted__isnull=True)
        serializer = MaterialListSerializer(queryset, many=True)
        return Response(serializer.data)


# Service ViewSet
class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de Service
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['sku', 'description', 'OBS']
    ordering_fields = ['description', 'gross_price', 'created_at']
    ordering = ['description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer

    def get_queryset(self):
        """
        Filtrar servicios eliminados por defecto
        """
        queryset = super().get_queryset()
        if not self.request.query_params.get('include_deleted'):
            queryset = queryset.filter(is_deleted__isnull=True)
        return queryset

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo servicios activos
        """
        queryset = self.queryset.filter(is_active=True, is_deleted__isnull=True)
        serializer = ServiceListSerializer(queryset, many=True)
        return Response(serializer.data)
