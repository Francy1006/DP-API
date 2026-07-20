from django.test import SimpleTestCase
from django.urls import reverse

from pricing.models import PriceConfiguration
from pricing.serializers import PriceConfigurationSerializer
from pricing.views import PriceConfigurationViewSet


class PriceConfigurationContractTests(SimpleTestCase):
    def test_model_maps_the_flyway_owned_table_and_relationships(self):
        self.assertFalse(PriceConfiguration._meta.managed)
        self.assertEqual(
            PriceConfiguration._meta.db_table,
            '"ditaly_pasta"."price_configuration"',
        )
        self.assertEqual(
            PriceConfiguration._meta.get_field('franchise_configuration').target_field.name,
            'code',
        )
        self.assertEqual(
            PriceConfiguration._meta.get_field('variable_formula').target_field.name,
            'code',
        )
        self.assertEqual(
            PriceConfiguration._meta.get_field('record_type').target_field.name,
            'id',
        )

    def test_serializer_exposes_the_crud_contract(self):
        fields = PriceConfigurationSerializer().fields

        for field_name in [
            'id', 'code', 'price_configuration', 'franchise_configuration',
            'variable_formula', 'record_type', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
        ]:
            self.assertIn(field_name, fields)

        self.assertTrue(fields['id'].read_only)
        self.assertTrue(fields['code'].read_only)
        self.assertTrue(fields['created_at'].read_only)

    def test_singular_routes_and_crud_methods_are_available(self):
        self.assertEqual(
            reverse('priceconfiguration-list'),
            '/api/price-configuration/',
        )
        self.assertEqual(
            reverse('priceconfiguration-detail', args=[1]),
            '/api/price-configuration/1/',
        )
        self.assertEqual(
            PriceConfigurationViewSet.http_method_names,
            ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'],
        )
