from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User, UserType, UserToken
from .serializers import UserSerializer, UserTypeSerializer, UserTokenSerializer
from django.utils import timezone

# Create your views here.

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type', 'description']
    ordering_fields = ['type', 'created_at']
    ordering = ['type']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_confirmed', 'is_deleted']
    search_fields = ['name', 'last_name', 'mail', 'google_id']
    ordering_fields = ['name', 'last_name', 'created_at', 'updated_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo usuarios activos"""
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed(self, request):
        """Obtener solo usuarios confirmados"""
        queryset = self.get_queryset().filter(is_confirmed=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserTokenViewSet(viewsets.ModelViewSet):
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id', 'revoked_at']
    search_fields = ['user_id__name', 'user_id__mail']
    ordering_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo tokens activos (no revocados)"""
        queryset = self.get_queryset().filter(revoked_at__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Revocar un token"""
        token = self.get_object()
        token.revoked_at = timezone.now()
        token.save()
        return Response({'status': 'token revoked'}, status=status.HTTP_200_OK)
