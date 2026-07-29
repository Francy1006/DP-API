from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from pricing.domain.entities import Price, PriceComponents, PriceConfiguration
from pricing.domain.exceptions import (
    CurrentPriceNotFound,
    FiscalDirectiveUnavailable,
    UnsafeCurrentPrice,
)
from products.domain.exceptions import ProductPriceConfigurationUnavailable
from products.infrastructure.repositories import django_price_repository
from products.infrastructure.repositories.django_price_repository import (
    DjangoPriceRepository,
)


CREATED_AT = datetime(2026, 7, 29, 12, 30, tzinfo=timezone.utc)
PRICE_CODE = "price-code"
PRODUCT_CODE = "product-code"
CONFIGURATION_CODE = "configuration-code"
CREATED_BY = "user-code"


def build_price_model(**overrides):
    values = {
        "code": PRICE_CODE,
        "base_net_amount": Decimal("1000.00"),
        "net_amount": Decimal("1000.00"),
        "gross_amount": Decimal("1190.00"),
        "iva_amount": Decimal("190.00"),
        "aditional_tax_amount": Decimal("0.00"),
        "retention_amount": Decimal("0.00"),
        "price_configuration": CONFIGURATION_CODE,
        "is_current": True,
        "is_deleted": False,
        "is_confirmed": True,
        "created_at": CREATED_AT,
        "created_by_id": CREATED_BY,
        "record_item_code": PRODUCT_CODE,
        "price_record_type": 1,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def expected_price(**overrides):
    values = {
        "code": PRICE_CODE,
        "base_net_amount": Decimal("1000.00"),
        "net_amount": Decimal("1000.00"),
        "gross_amount": Decimal("1190.00"),
        "iva_amount": Decimal("190.00"),
        "aditional_tax_amount": Decimal("0.00"),
        "retention_amount": Decimal("0.00"),
        "price_configuration": CONFIGURATION_CODE,
        "is_current": True,
        "is_deleted": False,
        "is_confirmed": True,
        "created_at": CREATED_AT,
        "created_by": CREATED_BY,
        "record_item_code": PRODUCT_CODE,
        "price_record_type": 1,
    }
    values.update(overrides)
    return Price(**values)


class DjangoPriceRepositoryTests(SimpleTestCase):
    def setUp(self):
        self.repository = DjangoPriceRepository()

    def test_to_entity_maps_every_price_field(self):
        entity = self.repository._to_entity(build_price_model())

        self.assertEqual(entity, expected_price())

    @patch.object(django_price_repository.PriceModel, "objects")
    def test_get_for_update_locks_and_returns_the_mapped_price(self, price_manager):
        model = build_price_model()
        locked_queryset = price_manager.select_for_update.return_value
        locked_queryset.get.return_value = model

        result = self.repository.get_for_update(PRICE_CODE)

        price_manager.select_for_update.assert_called_once_with()
        locked_queryset.get.assert_called_once_with(code=PRICE_CODE)
        self.assertEqual(result, expected_price())

    @patch.object(django_price_repository.PriceModel, "objects")
    def test_get_for_update_translates_a_missing_price(self, price_manager):
        price_manager.select_for_update.return_value.get.side_effect = (
            django_price_repository.PriceModel.DoesNotExist
        )

        with self.assertRaises(CurrentPriceNotFound):
            self.repository.get_for_update(PRICE_CODE)

    @patch.object(django_price_repository.ProductModel, "objects")
    def test_count_product_references_includes_every_foreign_key(self, product_manager):
        referenced_products = product_manager.filter.return_value
        referenced_products.count.return_value = 3

        result = self.repository.count_product_references(PRICE_CODE)

        product_manager.filter.assert_called_once_with(price_id=PRICE_CODE)
        referenced_products.count.assert_called_once_with()
        self.assertEqual(result, 3)

    @patch.object(django_price_repository, "connection")
    def test_get_product_configuration_maps_the_single_active_result(self, connection):
        database_cursor = connection.cursor.return_value.__enter__.return_value
        database_cursor.fetchall.return_value = [
            (
                CONFIGURATION_CODE,
                "Product price",
                1,
                "formula-code",
                "Standard formula",
                "gross_amount=${net_amount}*(1+${iva});",
            )
        ]

        result = self.repository.get_product_configuration(CONFIGURATION_CODE)

        query, parameters = database_cursor.execute.call_args.args
        self.assertIn("FROM ditaly_pasta.price_configuration", query)
        self.assertIn("ft.type = 'PRICE'", query)
        self.assertEqual(parameters, [CONFIGURATION_CODE, 1])
        self.assertEqual(
            result,
            PriceConfiguration(
                code=CONFIGURATION_CODE,
                name="Product price",
                record_type=1,
                variable_formula_code="formula-code",
                variable_formula_name="Standard formula",
                formula_template="gross_amount=${net_amount}*(1+${iva});",
            ),
        )

    @patch.object(django_price_repository, "connection")
    def test_get_product_configuration_rejects_invalid_cardinality(self, connection):
        database_cursor = connection.cursor.return_value.__enter__.return_value
        valid_row = (
            CONFIGURATION_CODE,
            "Product price",
            1,
            "formula-code",
            "Standard formula",
            "gross_amount=${net_amount}*(1+${iva});",
        )

        for rows in ([], [valid_row, valid_row]):
            with self.subTest(row_count=len(rows)):
                database_cursor.fetchall.return_value = rows
                with self.assertRaises(ProductPriceConfigurationUnavailable):
                    self.repository.get_product_configuration(CONFIGURATION_CODE)

    @patch.object(django_price_repository, "connection")
    def test_get_formula_variables_converts_values_to_decimal(self, connection):
        database_cursor = connection.cursor.return_value.__enter__.return_value
        database_cursor.fetchall.return_value = [
            ("iva", "0.190"),
            ("retention", Decimal("0.015")),
        ]

        result = self.repository.get_formula_variables(CONFIGURATION_CODE)

        query, parameters = database_cursor.execute.call_args.args
        self.assertIn(
            "FROM ditaly_pasta.fiscal_configuration_detail",
            query,
        )
        self.assertEqual(parameters, [CONFIGURATION_CODE])
        self.assertEqual(
            result,
            {
                "iva": Decimal("0.190"),
                "retention": Decimal("0.015"),
            },
        )

    @patch.object(django_price_repository, "connection")
    def test_get_formula_variables_rejects_incomplete_or_duplicated_rows(
        self,
        connection,
    ):
        database_cursor = connection.cursor.return_value.__enter__.return_value
        invalid_result_sets = (
            [("", "0.190")],
            [("iva", None)],
            [("iva", "0.190"), ("iva", "0.200")],
        )

        for rows in invalid_result_sets:
            with self.subTest(rows=rows):
                database_cursor.fetchall.return_value = rows
                with self.assertRaises(FiscalDirectiveUnavailable):
                    self.repository.get_formula_variables(CONFIGURATION_CODE)

    @patch.object(django_price_repository, "uuid4")
    @patch.object(django_price_repository.PriceModel, "objects")
    def test_create_version_persists_and_maps_the_new_current_price(
        self,
        price_manager,
        uuid4,
    ):
        uuid4.return_value = "generated-price-code"
        created_model = build_price_model(code="generated-price-code")
        price_manager.create.return_value = created_model
        components = PriceComponents(
            gross_amount=Decimal("1190.00"),
            base_net_amount=Decimal("1000.00"),
            net_amount=Decimal("1000.00"),
            iva_amount=Decimal("190.00"),
            aditional_tax_amount=Decimal("0.00"),
            retention_amount=Decimal("0.00"),
        )

        result = self.repository.create_version(
            components=components,
            configuration_code=CONFIGURATION_CODE,
            product_code=PRODUCT_CODE,
            created_at=CREATED_AT,
            created_by=CREATED_BY,
        )

        price_manager.create.assert_called_once_with(
            code="generated-price-code",
            base_net_amount=Decimal("1000.00"),
            net_amount=Decimal("1000.00"),
            gross_amount=Decimal("1190.00"),
            iva_amount=Decimal("190.00"),
            aditional_tax_amount=Decimal("0.00"),
            retention_amount=Decimal("0.00"),
            price_configuration=CONFIGURATION_CODE,
            is_current=True,
            created_at=CREATED_AT,
            created_by_id=CREATED_BY,
            record_item_code=PRODUCT_CODE,
            price_record_type=1,
        )
        self.assertEqual(
            result,
            expected_price(code="generated-price-code"),
        )

    @patch.object(django_price_repository.PriceModel, "objects")
    def test_deactivate_updates_the_single_current_price(self, price_manager):
        current_prices = price_manager.filter.return_value
        current_prices.update.return_value = 1

        self.repository.deactivate(PRICE_CODE)

        price_manager.filter.assert_called_once_with(
            code=PRICE_CODE,
            is_current=True,
        )
        current_prices.update.assert_called_once_with(is_current=False)

    @patch.object(django_price_repository.PriceModel, "objects")
    def test_deactivate_rejects_unsafe_update_counts(self, price_manager):
        current_prices = price_manager.filter.return_value

        for updated_count in (0, 2):
            with self.subTest(updated_count=updated_count):
                current_prices.update.return_value = updated_count
                with self.assertRaises(UnsafeCurrentPrice):
                    self.repository.deactivate(PRICE_CODE)
