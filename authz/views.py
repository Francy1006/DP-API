from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import Role, Permission, PermissionType, RolePermissions, Restriction, RestrictionRoles
from .serializers import (
    RoleSerializer, PermissionSerializer, PermissionTypeSerializer,
    RolePermissionsSerializer, RestrictionSerializer, RestrictionRolesSerializer
)

# Create your views here.

class PermissionTypeViewSet(viewsets.ModelViewSet):
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'created_at']
    ordering = ['type']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo tipos de permisos activos"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo tipos de permisos confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_deleted', 'is_confirmed']
    search_fields = ['permission', 'description']
    ordering_fields = ['permission', 'created_at']
    ordering = ['permission']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo permisos activos"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo permisos confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['role', 'description']
    ordering_fields = ['role', 'created_at']
    ordering = ['role']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo roles activos"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo roles confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RolePermissionsViewSet(viewsets.ModelViewSet):
    queryset = RolePermissions.objects.all()
    serializer_class = RolePermissionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'permission', 'is_deleted', 'is_confirmed']
    search_fields = ['role__role', 'permission__permission']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo relaciones activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo relaciones confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RestrictionViewSet(viewsets.ModelViewSet):
    queryset = Restriction.objects.all()
    serializer_class = RestrictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['restriction', 'description']
    ordering_fields = ['restriction', 'created_at']
    ordering = ['restriction']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo restricciones activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo restricciones confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RestrictionRolesViewSet(viewsets.ModelViewSet):
    queryset = RestrictionRoles.objects.all()
    serializer_class = RestrictionRolesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restriction', 'role', 'is_deleted', 'is_confirmed']
    search_fields = ['restriction__restriction', 'role__role']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo relaciones activas"""
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo relaciones confirmadas"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
