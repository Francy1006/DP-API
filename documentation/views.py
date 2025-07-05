from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import InstructionType, Instruction
from .serializers import InstructionTypeSerializer, InstructionSerializer

# Create your views here.

class InstructionTypeViewSet(viewsets.ModelViewSet):
    queryset = InstructionType.objects.all()
    serializer_class = InstructionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'created_at']
    ordering = ['type']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo tipos de instrucciones activos"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo tipos de instrucciones confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['instruction', 'description']
    ordering_fields = ['instruction', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo instrucciones activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo instrucciones confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirmar una instrucción"""
        instruction = self.get_object()
        instruction.is_confirmed = True
        instruction.confirmed_at = timezone.now()
        instruction.confirmed_by = request.user
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """Eliminación suave de una instrucción"""
        instruction = self.get_object()
        instruction.is_deleted = True
        instruction.deleted_at = timezone.now()
        instruction.deleted_by = request.user
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restaurar una instrucción eliminada"""
        instruction = self.get_object()
        instruction.is_deleted = False
        instruction.deleted_at = None
        instruction.deleted_by = None
        instruction.save()
        serializer = self.get_serializer(instruction)
        return Response(serializer.data)
