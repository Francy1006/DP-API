from decimal import Decimal

from django.test import SimpleTestCase

from products.presentation.serializers import (
    ProductCommandSerializer,
    ProductSerializer,
)


CONFIGURATION = "cd746343-baf4-4359-b2e6-9bd829631e30"


def test_product_response_contains_price_configuration_label(product_factory):
    response = ProductSerializer(product_factory()).data

    assert response["price_configuration"] == CONFIGURATION
    assert response["price_configuration_label"] == "PRODUCT_NORMAL_IVA"


class ProductSerializerContractTests(SimpleTestCase):
    expected_fields = [
        "id", "code", "sku", "description", "obs", "package_unit",
        "min_package_purchase", "price", "base_net_amount", "net_amount",
        "gross_amount", "iva_amount", "aditional_tax_amount",
        "retention_amount", "price_configuration",
        "price_configuration_label", "provider", "provider_name", "type",
        "type_name", "item_group", "item_group_name", "category",
        "category_name", "url", "package", "package_description",
        "is_active", "is_deleted", "is_confirmed", "created_at",
        "updated_at", "confirmed_at", "deleted_at", "created_by",
        "confirmed_by", "updated_by", "deleted_by", "version",
    ]

    def test_public_fields_remain_unchanged(self):
        self.assertEqual(list(ProductSerializer().fields), self.expected_fields)
        self.assertNotIn("log", ProductSerializer().fields)
        self.assertTrue(
            ProductSerializer().fields["price_configuration_label"].read_only
        )

    def test_confirmation_audit_fields_are_read_only(self):
        fields = ProductCommandSerializer().fields

        self.assertTrue(fields["sku"].read_only)
        self.assertTrue(fields["price"].read_only)
        self.assertTrue(fields["confirmed_at"].read_only)
        self.assertTrue(fields["confirmed_by"].read_only)
        self.assertFalse(fields["base_net_amount"].read_only)
        self.assertFalse(fields["price_configuration"].read_only)

    def test_product_response_contains_all_amounts_without_legacy_alias(self):
        fields = ProductSerializer().fields

        self.assertNotIn("price_gross_amount", fields)
        for field_name in (
            "base_net_amount", "net_amount", "gross_amount", "iva_amount",
            "aditional_tax_amount", "retention_amount", "price_configuration",
            "price_configuration_label",
        ):
            self.assertIn(field_name, fields)

    def test_base_accepts_two_decimals_and_configuration_is_writable(self):
        serializer = ProductCommandSerializer(
            data={
                "base_net_amount": "20000.25",
                "price_configuration": CONFIGURATION,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["base_net_amount"], Decimal("20000.25")
        )
        self.assertEqual(
            serializer.validated_data["price_configuration"], CONFIGURATION
        )

    def test_rejects_invalid_base_amounts(self):
        for invalid in (None, "invalid", 0, -1, "10.001"):
            with self.subTest(value=invalid):
                serializer = ProductCommandSerializer(
                    data={"base_net_amount": invalid}, partial=True
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn("base_net_amount", serializer.errors)

    def test_rejects_direct_price_and_derived_amount_changes(self):
        for field_name in (
            "price", "net_amount", "gross_amount", "iva_amount",
            "aditional_tax_amount", "retention_amount", "record_item_code",
            "price_record_type", "is_current",
        ):
            with self.subTest(field=field_name):
                serializer = ProductCommandSerializer(
                    data={field_name: "forged"}, partial=True
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn(field_name, serializer.errors)

    def test_product_post_requires_base_and_price_configuration(self):
        serializer = ProductCommandSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("base_net_amount", serializer.errors)
        self.assertIn("price_configuration", serializer.errors)

    def test_response_uses_canonical_relationship_names_and_labels(self):
        fields = ProductSerializer().fields

        self.assertIn("item_group", fields)
        self.assertIn("item_group_name", fields)
        self.assertIn("provider_name", fields)
        self.assertIn("type_name", fields)
        self.assertIn("category_name", fields)
        self.assertIn("package_description", fields)
        self.assertNotIn("group", fields)
        self.assertNotIn("group_name", fields)

    def test_confirmation_audit_payload_is_ignored_by_command_serializer(self):
        serializer = ProductCommandSerializer(
            data={
                "confirmed_at": "2026-01-01T00:00:00Z",
                "confirmed_by": "forged-user",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("confirmed_at", serializer.validated_data)
        self.assertNotIn("confirmed_by", serializer.validated_data)
