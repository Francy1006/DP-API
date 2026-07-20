from rest_framework import serializers
from .models import (
    FiscalDirectiveType, FiscalDirective, FiscalFormula, 
    PriceFiscalConfiguration, PriceConfiguration, Price,
    FiscalConfigurationDetail
)

class FiscalDirectiveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalDirectiveType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class FiscalDirectiveSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = FiscalDirective
        fields = [
            'id', 'code', 'obs', 'fiscal_directive', 'type', 'type_name',
            'percentage', 'official_source_url', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class FiscalFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalFormula
        fields = [
            'id', 'formula', 'formula_template', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PriceFiscalConfigurationSerializer(serializers.ModelSerializer):
    fiscal_formula_name = serializers.CharField(source='fiscal_formula.formula', read_only=True)
    
    class Meta:
        model = PriceFiscalConfiguration
        fields = [
            'id', 'fiscal_configuration', 'fiscal_formula', 'fiscal_formula_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PriceConfigurationSerializer(serializers.ModelSerializer):
    franchise_configuration_name = serializers.CharField(
        source='franchise_configuration.configuration', read_only=True
    )
    variable_formula_name = serializers.CharField(
        source='variable_formula.formula', read_only=True
    )
    record_type_name = serializers.CharField(
        source='record_type.type', read_only=True
    )

    class Meta:
        model = PriceConfiguration
        fields = [
            'id', 'code', 'price_configuration',
            'franchise_configuration', 'franchise_configuration_name',
            'variable_formula', 'variable_formula_name',
            'record_type', 'record_type_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by',
        ]
        read_only_fields = [
            'id', 'code', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at',
        ]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'id', 'code', 'base_net_amount', 'net_amount', 'gross_amount',
            'iva_amount', 'aditional_tax_amount', 'retention_amount',
            'price_configuration', 'is_current', 'is_deleted', 'is_confirmed',
            'created_at', 'created_by', 'record_item_code', 'price_record_type',
        ]
        read_only_fields = ['id', 'created_at']


class FiscalConfigurationDetailSerializer(serializers.ModelSerializer):
    price_fiscal_configuration_name = serializers.CharField(source='price_fiscal_configuration.fiscal_configuration', read_only=True)
    price_code = serializers.CharField(source='price.code', read_only=True)
    fiscal_directive_name = serializers.CharField(source='fiscal_directive.fiscal_directive', read_only=True)
    
    class Meta:
        model = FiscalConfigurationDetail
        fields = [
            'id', 'price_fiscal_configuration', 'price_fiscal_configuration_name',
            'price', 'price_code', 'fiscal_directive', 'fiscal_directive_name', 'log'
        ]
        read_only_fields = ['id']
