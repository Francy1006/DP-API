from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import serializers

from pricing.domain.exceptions import (
    ProductPriceConfigurationUnavailable,
    UnsafeCurrentPrice,
)
from products.presentation.views import PriceVersionConflict, ProductViewSet


class ProductViewContractTests(SimpleTestCase):
    def test_routes_and_methods_remain_unchanged(self):
        self.assertEqual(
            ProductViewSet.http_method_names,
            ["get", "post", "patch", "head", "options"],
        )
        self.assertEqual(reverse("product-list"), "/api/products/")
        self.assertEqual(reverse("product-detail", args=[1]), "/api/products/1/")
        self.assertEqual(
            reverse("product-delete", args=[1]), "/api/products/1/delete/"
        )
        self.assertEqual(reverse("product-active"), "/api/products/active/")

    def test_pricing_conflicts_map_to_http_409(self):
        with self.assertRaises(PriceVersionConflict) as raised:
            ProductViewSet._raise_api_error(UnsafeCurrentPrice())

        self.assertEqual(raised.exception.status_code, 409)

    def test_unavailable_product_configuration_maps_to_its_request_field(self):
        with self.assertRaises(serializers.ValidationError) as raised:
            ProductViewSet._raise_api_error(
                ProductPriceConfigurationUnavailable()
            )

        self.assertIn("price_configuration", raised.exception.detail)
