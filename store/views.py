from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction
from .serializers import (
    ItemGroupSerializer, ItemGroupListSerializer,
    MenuSerializer, MenuListSerializer,
    ItemCategorySerializer, ItemCategoryListSerializer,
    ItemTypeSerializer, ItemTypeListSerializer,
    InstructionTypeSerializer, InstructionTypeListSerializer,
    InstructionSerializer, InstructionListSerializer,
    InstructionCreateSerializer, InstructionUpdateSerializer
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


# ItemGroup ViewSet (existing)
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
