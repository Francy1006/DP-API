from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.test import SimpleTestCase

from products.models import Product


class ProductModelMappingTests(SimpleTestCase):
    def test_product_model_maps_unmanaged_product_table(self):
        self.assertFalse(Product._meta.managed)
        self.assertEqual(Product._meta.db_table, "product")

    def test_product_model_uses_canonical_item_group_column(self):
        field = Product._meta.get_field("item_group")

        self.assertEqual(field.column, "item_group")
        with self.assertRaises(FieldDoesNotExist):
            Product._meta.get_field("group")

    def test_product_model_maps_price_code_with_protect(self):
        field = Product._meta.get_field("price")

        self.assertEqual(field.target_field.name, "code")
        self.assertIs(field.remote_field.on_delete, models.PROTECT)
