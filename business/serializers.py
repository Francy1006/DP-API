from rest_framework import serializers
from .models import ItemFilterClassification


class ItemFilterClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFilterClassification
        fields = ['id', 'classification', 'description']
        read_only_fields = ['id']


