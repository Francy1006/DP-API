from rest_framework import serializers
from .models import Ticket
from pricing.models import Price


class TicketSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    item_group_name = serializers.CharField(source='item_group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    filter_classification_name = serializers.CharField(source='filter_classification.classification', read_only=True)
    package_description = serializers.CharField(source='package.description', read_only=True)
    price = serializers.SerializerMethodField()
    
    def get_price(self, obj):
        """Obtener el valor del precio desde la tabla Price relacionada"""
        if not obj.price:
            return None
        
        # Usar el diccionario de precios del contexto si está disponible (para evitar N+1 queries)
        prices_dict = self.context.get('prices_dict', {})
        if prices_dict and obj.price in prices_dict:
            return prices_dict[obj.price]
        
        # Fallback: consulta individual si no hay contexto (para otros endpoints)
        try:
            price_obj = Price.objects.get(code=obj.price)
            # Retornar gross_amount como el valor del precio
            # Si necesitas otro campo (net_amount, iva_amount, etc.), cambia aquí
            return price_obj.gross_amount
        except Price.DoesNotExist:
            return None
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'code', 'sku', 'description', 'cover_image', 'secondary_image',
            'complementary_image', 'image_gallery', 'obs', 'package_unit',
            'min_package_purchase', 'price', 'type', 'type_name', 'item_group',
            'item_group_name', 'category', 'category_name', 'filter_classification',
            'filter_classification_name', 'url', 'package', 'package_description',
            'is_active', 'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by', 'updated_by',
            'deleted_by', 'log', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']





