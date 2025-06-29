from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ItemGroup
from .serializers import ItemGroupSerializer, ItemGroupListSerializer


class ItemGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD completas de ItemGroup
    """
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cataloge_render']
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
        queryset = self.queryset.filter(cataloge_render=True)
        serializer = ItemGroupListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_catalog_render(self, request, pk=None):
        """
        Endpoint para alternar el estado de renderizado en catálogo
        """
        item_group = self.get_object()
        item_group.cataloge_render = not item_group.cataloge_render
        item_group.save()
        serializer = self.get_serializer(item_group)
        return Response(serializer.data)


# Vistas individuales para mayor control si es necesario
from rest_framework.views import APIView


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
