from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Ticket
from .serializers import TicketSerializer
from pricing.models import Price


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        'type', 'item_group', 'category', 'filter_classification', 'package'
    ).all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'item_group', 'category', 'filter_classification', 'package', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'sku', 'description']
    ordering_fields = ['description', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo tickets activos"""
        active_tickets = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def web(self, request):
        """Obtener tickets cuyo SKU comienza con 'DP00-' ordenados por SKU ascendente"""
        web_tickets_queryset = self.queryset.filter(sku__startswith='DP00-').order_by('sku')
        
        # Obtener los códigos de precio únicos usando una consulta separada (más eficiente)
        price_codes = list(web_tickets_queryset.values_list('price', flat=True).distinct())
        price_codes = [code for code in price_codes if code and code.strip()]  # Filtrar None/empty/whitespace
        
        # Crear diccionario de precios si hay códigos
        prices_dict = {}
        if price_codes:
            prices = Price.objects.filter(code__in=price_codes).only('code', 'gross_amount')
            prices_dict = {price.code: price.gross_amount for price in prices}
        
        # Pasar el diccionario de precios al contexto del serializer
        serializer = self.get_serializer(web_tickets_queryset, many=True, context={'prices_dict': prices_dict})
        return Response(serializer.data)

