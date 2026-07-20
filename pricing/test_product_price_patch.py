from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal

from django.test import SimpleTestCase
from rest_framework import serializers

from pricing.domain.entities import Price, ProductPriceConfiguration
from pricing.domain.exceptions import (
    ProductPriceConfigurationUnavailable,
    UnsafeCurrentPrice,
)
from products.application.commands import CreateProductCommand, UpdateProductCommand
from products.application.use_cases import CreateProduct, UpdateProduct
from products.domain.entities import Product
from products.presentation.serializers import (
    ProductCommandSerializer,
    ProductSerializer,
)
from products.presentation.views import PriceVersionConflict, ProductViewSet


ACTOR = "5fbf2886-4ad0-11f0-8ce6-0242ac120002"
PRODUCT_CODE = "7d211027-f191-4049-8335-480158a28acf"
OLD_PRICE_CODE = "bf397d95-c18c-4620-88c9-af621f553951"
NEW_PRICE_CODE = "9c238044-8110-4da8-8461-7b51cf3c750e"
CONFIGURATION_CODE = "cd746343-baf4-4359-b2e6-9bd829631e30"
NOW = datetime(2026, 7, 17, 18, 30, tzinfo=timezone.utc)
STANDARD_FORMULA = (
    "net_amount=${net_amount};"
    "iva_amount=${net_amount}*${iva};"
    "gross_amount=${net_amount}*(1+${iva});"
)


class FixedClock:
    def now(self):
        return NOW

    def format_log_timestamp(self, value):
        return "2026-07-17 18:30:00.000"


def product_entity():
    return Product(
        id=4,
        code=PRODUCT_CODE,
        sku="P-001-0001",
        description="Producto",
        obs="Observación",
        package_unit=1,
        min_package_purchase=1,
        price=OLD_PRICE_CODE,
        base_net_amount=Decimal("16980"),
        net_amount=Decimal("16980"),
        gross_amount=Decimal("20206.20"),
        iva_amount=Decimal("3226.20"),
        aditional_tax_amount=Decimal("0"),
        retention_amount=Decimal("0"),
        price_configuration=CONFIGURATION_CODE,
        price_configuration_label="PRODUCT_NORMAL_IVA",
        provider=1,
        type=1,
        item_group=6,
        category=8,
        package=1,
        created_by=ACTOR,
        log="init;",
    )


def current_price(record_item_code=PRODUCT_CODE):
    return Price(
        code=OLD_PRICE_CODE,
        base_net_amount=Decimal("16980.00"),
        net_amount=Decimal("16980.00"),
        gross_amount=Decimal("20206.20"),
        iva_amount=Decimal("3226.20"),
        aditional_tax_amount=Decimal("0.00"),
        retention_amount=Decimal("0.00"),
        price_configuration=CONFIGURATION_CODE,
        is_current=True,
        is_deleted=None,
        is_confirmed=None,
        created_at=NOW,
        created_by=ACTOR,
        record_item_code=record_item_code,
        price_record_type=1,
    )


class FakeProductRepository:
    def __init__(self):
        self.product = product_entity()
        self.updated_fields = None
        self.fail_update = False
        self.fail_create = False

    def user_exists(self, user_code):
        return user_code == ACTOR

    def get(self, product_id):
        return self.product

    def get_for_update(self, product_id):
        return self.product

    def update(self, product, changed_fields):
        if self.fail_update:
            raise RuntimeError("intermediate persistence error")
        self.product = product
        self.updated_fields = changed_fields
        return product

    def create(self, product):
        if self.fail_create:
            raise RuntimeError("product create failed")
        product.id = 5
        self.product = product
        return product


class FakePriceRepository:
    def __init__(self, price=None, references=1):
        self.current = price or current_price()
        self.references = references
        self.created = []
        self.deactivated = []

    def get_for_update(self, price_code):
        return self.current

    def count_product_references(self, price_code):
        return self.references

    def get_product_configuration(self, configuration_code):
        return ProductPriceConfiguration(
            code=configuration_code,
            name="PRODUCT_NORMAL_IVA",
            record_type=1,
            variable_formula_code="210bbae6-1e2b-4b09-93ee-f26d08cb6be1",
            variable_formula_name="PRODUCT_STANDARD",
            formula_template=STANDARD_FORMULA,
        )

    def get_formula_variables(self, configuration_code):
        return {"iva": Decimal("0.190")}

    def create_version(
        self,
        components,
        configuration_code,
        product_code,
        created_at,
        created_by,
    ):
        price = Price(
            code=NEW_PRICE_CODE,
            base_net_amount=components.base_net_amount,
            net_amount=components.net_amount,
            gross_amount=components.gross_amount,
            iva_amount=components.iva_amount,
            aditional_tax_amount=components.aditional_tax_amount,
            retention_amount=components.retention_amount,
            price_configuration=configuration_code,
            is_current=True,
            is_deleted=None,
            is_confirmed=None,
            created_at=created_at,
            created_by=created_by,
            record_item_code=product_code,
            price_record_type=1,
        )
        self.created.append(price)
        return price

    def deactivate(self, price_code):
        self.deactivated.append(price_code)


class SnapshotTransactionManager:
    def __init__(self, product_repository, price_repository):
        self.product_repository = product_repository
        self.price_repository = price_repository

    @contextmanager
    def atomic(self):
        product_snapshot = deepcopy(self.product_repository.__dict__)
        price_snapshot = deepcopy(self.price_repository.__dict__)
        try:
            yield
        except Exception:
            self.product_repository.__dict__.clear()
            self.product_repository.__dict__.update(product_snapshot)
            self.price_repository.__dict__.clear()
            self.price_repository.__dict__.update(price_snapshot)
            raise


def use_case(product_repository, price_repository):
    return UpdateProduct(
        repository=product_repository,
        price_repository=price_repository,
        transaction_manager=SnapshotTransactionManager(
            product_repository,
            price_repository,
        ),
        clock=FixedClock(),
    )


class ProductPricePatchUseCaseTests(SimpleTestCase):
    def test_new_base_creates_and_links_a_complete_price_version(self):
        products = FakeProductRepository()
        prices = FakePriceRepository()

        result = use_case(products, prices).execute(
            UpdateProductCommand(
                product_id=4,
                changes={"base_net_amount": Decimal("20000.25")},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(len(prices.created), 1)
        created = prices.created[0]
        self.assertEqual(created.base_net_amount, Decimal("20000.25"))
        self.assertEqual(created.net_amount, Decimal("20000.25"))
        self.assertEqual(created.iva_amount, Decimal("3800.05"))
        self.assertEqual(created.gross_amount, Decimal("23800.30"))
        self.assertEqual(created.price_configuration, CONFIGURATION_CODE)
        self.assertEqual(created.record_item_code, PRODUCT_CODE)
        self.assertEqual(created.price_record_type, 1)
        self.assertTrue(created.is_current)
        self.assertEqual(created.created_at, NOW)
        self.assertEqual(created.created_by, ACTOR)
        self.assertEqual(prices.deactivated, [OLD_PRICE_CODE])
        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(result.base_net_amount, Decimal("20000.25"))
        self.assertEqual(result.gross_amount, Decimal("23800.30"))
        self.assertEqual(result.updated_at, NOW)
        self.assertEqual(result.updated_by, ACTOR)
        self.assertEqual(result.version, 2)
        self.assertIn("base_net_amount=20000.25", products.product.log)
        self.assertTrue(products.product.log.endswith(";"))

    def test_same_persisted_result_is_idempotent(self):
        products = FakeProductRepository()
        prices = FakePriceRepository(references=6)

        result = use_case(products, prices).execute(
            UpdateProductCommand(
                product_id=4,
                changes={"base_net_amount": Decimal("16980.00")},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(prices.created, [])
        self.assertEqual(prices.deactivated, [])
        self.assertEqual(result.price, OLD_PRICE_CODE)
        self.assertEqual(result.version, 1)
        self.assertIn("PATCH: sin cambios", products.product.log)

    def test_configuration_change_versions_even_with_the_same_base(self):
        products = FakeProductRepository()
        prices = FakePriceRepository()
        other_configuration = "11111111-2222-3333-4444-555555555555"

        result = use_case(products, prices).execute(
            UpdateProductCommand(
                product_id=4,
                changes={"price_configuration": other_configuration},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(len(prices.created), 1)
        self.assertEqual(
            prices.created[0].price_configuration,
            other_configuration,
        )
        self.assertEqual(result.price_configuration, other_configuration)
        self.assertEqual(result.version, 2)
        self.assertEqual(prices.deactivated, [OLD_PRICE_CODE])

    def test_shared_or_inconsistently_owned_price_is_forked_safely(self):
        scenarios = (
            FakePriceRepository(references=6),
            FakePriceRepository(
                price=current_price(record_item_code="another-product")
            ),
            FakePriceRepository(
                price=Price(
                    **{
                        **current_price().__dict__,
                        "price_record_type": 4,
                    }
                )
            ),
        )
        for prices in scenarios:
            products = FakeProductRepository()
            with self.subTest(price=prices.current.record_item_code):
                result = use_case(products, prices).execute(
                    UpdateProductCommand(
                        product_id=4,
                        changes={"base_net_amount": Decimal("20000")},
                        updated_by=ACTOR,
                    )
                )

                self.assertEqual(len(prices.created), 1)
                self.assertEqual(prices.deactivated, [])
                self.assertEqual(products.product.price, NEW_PRICE_CODE)
                self.assertEqual(result.price, NEW_PRICE_CODE)
                self.assertEqual(
                    prices.created[0].record_item_code,
                    PRODUCT_CODE,
                )
                self.assertEqual(prices.created[0].price_record_type, 1)

    def test_configuration_change_forks_a_shared_price(self):
        products = FakeProductRepository()
        prices = FakePriceRepository(references=6)
        other_configuration = "11111111-2222-3333-4444-555555555555"

        result = use_case(products, prices).execute(
            UpdateProductCommand(
                product_id=4,
                changes={"price_configuration": other_configuration},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(len(prices.created), 1)
        self.assertEqual(prices.deactivated, [])
        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(result.price_configuration, other_configuration)

    def test_intermediate_error_rolls_back_price_and_product_changes(self):
        products = FakeProductRepository()
        products.fail_update = True
        prices = FakePriceRepository()

        with self.assertRaises(RuntimeError):
            use_case(products, prices).execute(
                UpdateProductCommand(
                    product_id=4,
                    changes={"base_net_amount": Decimal("20000")},
                    updated_by=ACTOR,
                )
            )

        self.assertEqual(prices.created, [])
        self.assertEqual(prices.deactivated, [])
        self.assertEqual(products.product.price, OLD_PRICE_CODE)
        self.assertEqual(products.product.base_net_amount, Decimal("16980.00"))

    def test_product_create_error_rolls_back_the_initial_price(self):
        products = FakeProductRepository()
        products.fail_create = True
        prices = FakePriceRepository()
        transaction_manager = SnapshotTransactionManager(products, prices)
        command = CreateProductCommand(
            code="new-product-code",
            description="Nuevo producto",
            obs="Prueba rollback",
            package_unit=1,
            min_package_purchase=1,
            base_net_amount=Decimal("20000.25"),
            price_configuration=CONFIGURATION_CODE,
            provider=1,
            type=1,
            item_group=6,
            category=8,
            package=1,
            created_by=ACTOR,
        )

        with self.assertRaises(RuntimeError):
            CreateProduct(
                repository=products,
                price_repository=prices,
                transaction_manager=transaction_manager,
                clock=FixedClock(),
            ).execute(command)

        self.assertEqual(prices.created, [])


class ProductPriceContractTests(SimpleTestCase):
    def test_product_response_contains_all_amounts_without_legacy_alias(self):
        fields = ProductSerializer().fields

        self.assertNotIn("price_gross_amount", fields)
        for field_name in (
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
            "price_configuration_label",
        ):
            self.assertIn(field_name, fields)

    def test_base_accepts_two_decimals_and_configuration_is_writable(self):
        serializer = ProductCommandSerializer(
            data={
                "base_net_amount": "20000.25",
                "price_configuration": CONFIGURATION_CODE,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["base_net_amount"],
            Decimal("20000.25"),
        )
        self.assertEqual(
            serializer.validated_data["price_configuration"],
            CONFIGURATION_CODE,
        )

    def test_rejects_invalid_base_amounts(self):
        for invalid in (None, "invalid", 0, -1, "10.001"):
            with self.subTest(value=invalid):
                serializer = ProductCommandSerializer(
                    data={"base_net_amount": invalid},
                    partial=True,
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn("base_net_amount", serializer.errors)

    def test_rejects_direct_price_and_derived_amount_changes(self):
        for field_name in (
            "price",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "record_item_code",
            "price_record_type",
            "is_current",
        ):
            with self.subTest(field=field_name):
                serializer = ProductCommandSerializer(
                    data={field_name: "forged"},
                    partial=True,
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn(field_name, serializer.errors)

    def test_product_post_requires_base_and_price_configuration(self):
        serializer = ProductCommandSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("base_net_amount", serializer.errors)
        self.assertIn("price_configuration", serializer.errors)

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
