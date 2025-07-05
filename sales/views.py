from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

# Esta app está preparada para futuras implementaciones de ventas
# Por ahora se mantiene vacía pero con la estructura base

class SalesBaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para entidades de ventas
    """
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    def get_queryset(self):
        return self.model.objects.none()
    
    def list(self, request, *args, **kwargs):
        return Response({"message": "Esta funcionalidad estará disponible próximamente"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def create(self, request, *args, **kwargs):
        return Response({"message": "Esta funcionalidad estará disponible próximamente"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def retrieve(self, request, *args, **kwargs):
        return Response({"message": "Esta funcionalidad estará disponible próximamente"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def update(self, request, *args, **kwargs):
        return Response({"message": "Esta funcionalidad estará disponible próximamente"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Esta funcionalidad estará disponible próximamente"}, status=status.HTTP_501_NOT_IMPLEMENTED)

# Create your views here.
