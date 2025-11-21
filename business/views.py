from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ItemFilterClassification
from .serializers import ItemFilterClassificationSerializer


class ItemFilterClassificationViewSet(viewsets.ModelViewSet):
    queryset = ItemFilterClassification.objects.all()
    serializer_class = ItemFilterClassificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = []
    search_fields = ['classification', 'description']
    ordering_fields = ['classification', 'id']
    ordering = ['classification']

    @action(detail=False, methods=['get'])
    def web(self, request):
        """
        Obtener todas las clasificaciones excluyendo las de tipo 'DEFAULT'
        """
        queryset = self.queryset.exclude(classification='DEFAULT')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

