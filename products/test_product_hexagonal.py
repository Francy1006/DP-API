from contextlib import nullcontext
from datetime import datetime, timezone
from decimal import Decimal

from django.test import SimpleTestCase
from django.urls import reverse

from products.application.commands import (
    CreateProductCommand,
    DeleteProductCommand,
    UpdateProductCommand,
)
from products.application.use_cases import CreateProduct, DeleteProduct, UpdateProduct
from products.domain.entities import Product
from products.domain.exceptions import ImmutableProductField
from products.presentation.serializers import (
    ProductCommandSerializer,
    ProductSerializer,
)
from products.presentation.views import ProductViewSet
from pricing.domain.entities import Price, ProductPriceConfiguration


ACTOR = "5fbf2886-4ad0-11f0-8ce6-0242ac120002"
NOW = datetime(2026, 7, 15, 17, 23, 13, 339000, tzinfo=timezone.utc)
CONFIGURATION = "cd746343-baf4-4359-b2e6-9bd829631e30"


class FixedClock:
    def now(self):
        return NOW

    def format_log_timestamp(self, value):
        return "2026-07-15 17:23:13.339"


class FakeProductRepository:
    def __init__(self, product=None):
        self.product = product
        self.submitted_sku = None

    def get(self, product_id):
        return self.product

    def get_for_update(self, product_id):
        return self.product

    def list(self, filters, search, ordering, active_only=False):
        return [self.product] if self.product else []

    def create(self, product):
        self.submitted_sku = product.sku
        if product.sku is None:
            product.sku = f"P-{product.provider:03d}-0001"
        product.id = 1
        self.product = product
        return product

    def update(self, product, changed_fields):
        self.product = product
        return product

    def soft_delete(self, product):
        self.product = product
        return product

    def user_exists(self, user_code):
        return user_code == ACTOR


class FakePriceRepository:
    def get_product_configuration(self, configuration_code):
        return ProductPriceConfiguration(
            code=CONFIGURATION,
            name="PRODUCT_NORMAL_IVA",
            record_type=1,
            variable_formula_code="210bbae6-1e2b-4b09-93ee-f26d08cb6be1",
            variable_formula_name="PRODUCT_STANDARD",
            formula_template=(
                "net_amount=${net_amount};"
                "iva_amount=${net_amount}*${iva};"
                "gross_amount=${net_amount}*(1+${iva});"
            ),
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
        return Price(
            code="new-price-code",
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


class FakeTransactionManager:
    def atomic(self):
        return nullcontext()


def create_product_use_case(repository):
    return CreateProduct(
        repository=repository,
        price_repository=FakePriceRepository(),
        transaction_manager=FakeTransactionManager(),
        clock=FixedClock(),
    )


def product_entity():
    return Product(
        id=1,
        code="3facdae4-c44e-475c-9911-d11b5fdf9980",
        sku="PRODUCTO-TEST",
        description="PRODUCTO DE VALIDACIÓN API",
        obs="REGISTRO TEMPORAL",
        package_unit=1,
        min_package_purchase=1,
        price="bf397d95-c18c-4620-88c9-af621f553951",
        provider=1,
        type=1,
        item_group=6,
        category=8,
        package=1,
        created_by=ACTOR,
        base_net_amount=Decimal("16980"),
        net_amount=Decimal("16980"),
        gross_amount=Decimal("20206.20"),
        iva_amount=Decimal("3226.20"),
        aditional_tax_amount=Decimal("0"),
        retention_amount=Decimal("0"),
        price_configuration=CONFIGURATION,
        price_configuration_label="PRODUCT_NORMAL_IVA",
        log="init;",
    )


class ProductContractTests(SimpleTestCase):
    expected_fields = [
        "id",
        "code",
        "sku",
        "description",
        "obs",
        "package_unit",
        "min_package_purchase",
        "price",
        "base_net_amount",
        "net_amount",
        "gross_amount",
        "iva_amount",
        "aditional_tax_amount",
        "retention_amount",
        "price_configuration",
        "price_configuration_label",
        "provider",
        "provider_name",
        "type",
        "type_name",
        "item_group",
        "item_group_name",
        "category",
        "category_name",
        "url",
        "package",
        "package_description",
        "is_active",
        "is_deleted",
        "is_confirmed",
        "created_at",
        "updated_at",
        "confirmed_at",
        "deleted_at",
        "created_by",
        "confirmed_by",
        "updated_by",
        "deleted_by",
        "version",
    ]

    def test_public_fields_and_methods_remain_unchanged(self):
        self.assertEqual(list(ProductSerializer().fields), self.expected_fields)
        self.assertNotIn("log", ProductSerializer().fields)
        self.assertTrue(
            ProductSerializer().fields["price_configuration_label"].read_only
        )
        self.assertEqual(
            ProductViewSet.http_method_names,
            ["get", "post", "patch", "head", "options"],
        )

    def test_product_response_contains_price_configuration_label(self):
        response = ProductSerializer(product_entity()).data

        self.assertEqual(response["price_configuration"], CONFIGURATION)
        self.assertEqual(
            response["price_configuration_label"],
            "PRODUCT_NORMAL_IVA",
        )

    def test_confirmation_audit_fields_are_read_only(self):
        fields = ProductCommandSerializer().fields

        self.assertTrue(fields["sku"].read_only)
        self.assertTrue(fields["price"].read_only)
        self.assertTrue(fields["confirmed_at"].read_only)
        self.assertTrue(fields["confirmed_by"].read_only)
        self.assertFalse(fields["base_net_amount"].read_only)
        self.assertFalse(fields["price_configuration"].read_only)

    def test_routes_remain_unchanged(self):
        self.assertEqual(reverse("product-list"), "/api/products/")
        self.assertEqual(reverse("product-detail", args=[1]), "/api/products/1/")
        self.assertEqual(
            reverse("product-delete", args=[1]), "/api/products/1/delete/"
        )
        self.assertEqual(reverse("product-active"), "/api/products/active/")


class ProductUseCaseTests(SimpleTestCase):
    def test_create_initializes_audit_log(self):
        repository = FakeProductRepository()
        command = CreateProductCommand(
            code="3facdae4-c44e-475c-9911-d11b5fdf9980",
            sku="PRODUCTO-TEST",
            description="PRODUCTO DE VALIDACIÓN API",
            obs="REGISTRO TEMPORAL",
            package_unit=1,
            min_package_purchase=1,
            base_net_amount=Decimal("16980.25"),
            price_configuration=CONFIGURATION,
            provider=1,
            type=1,
            item_group=6,
            category=8,
            package=1,
            created_by=ACTOR,
        )

        result = create_product_use_case(repository).execute(command)

        self.assertEqual(result.id, 1)
        self.assertEqual(result.sku, "P-001-0001")
        self.assertEqual(result.price, "new-price-code")
        self.assertEqual(result.base_net_amount, Decimal("16980.25"))
        self.assertEqual(result.gross_amount, Decimal("20206.50"))
        self.assertIsNone(repository.submitted_sku)
        self.assertFalse(result.is_confirmed)
        self.assertIsNone(result.confirmed_at)
        self.assertIsNone(result.confirmed_by)
        self.assertEqual(repository.product.created_at, NOW)
        self.assertEqual(
            repository.product.log,
            f"INIT: 2026-07-15 17:23:13.339 (USER: {ACTOR});",
        )

    def test_create_can_start_confirmed_with_automatic_audit(self):
        repository = FakeProductRepository()
        command = CreateProductCommand(
            code="3facdae4-c44e-475c-9911-d11b5fdf9980",
            sku="PRODUCTO-CONFIRMADO",
            description="PRODUCTO CONFIRMADO",
            obs="CONFIRMADO EN CREATE",
            package_unit=1,
            min_package_purchase=1,
            base_net_amount=Decimal("16980"),
            price_configuration=CONFIGURATION,
            provider=1,
            type=1,
            item_group=6,
            category=8,
            package=1,
            created_by=ACTOR,
            is_confirmed=True,
        )

        result = create_product_use_case(repository).execute(command)

        self.assertTrue(result.is_confirmed)
        self.assertEqual(result.confirmed_at, NOW)
        self.assertEqual(result.confirmed_by, ACTOR)
        self.assertEqual(
            repository.product.log,
            f"INIT: 2026-07-15 17:23:13.339 (USER: {ACTOR}) "
            "(confirmed);",
        )

    def test_patch_records_only_changed_values_and_terminates_log(self):
        repository = FakeProductRepository(product_entity())
        command = UpdateProductCommand(
            product_id=1,
            changes={
                "description": "descripción actualizada",
                "obs": "observaciones actualizada",
            },
            updated_by=ACTOR,
        )

        UpdateProduct(repository, None, None, FixedClock()).execute(command)

        self.assertEqual(
            repository.product.log,
            "init; PATCH: description='descripción actualizada', "
            f"obs='observaciones actualizada' (USER: {ACTOR});",
        )
        self.assertTrue(repository.product.log.endswith(";"))
        self.assertEqual(repository.product.version, 2)

        UpdateProduct(repository, None, None, FixedClock()).execute(
            UpdateProductCommand(
                product_id=1,
                changes={"obs": "segunda modificación"},
                updated_by=ACTOR,
            )
        )
        self.assertEqual(repository.product.version, 3)

    def test_patch_cannot_change_provider(self):
        repository = FakeProductRepository(product_entity())

        with self.assertRaises(ImmutableProductField) as raised:
            UpdateProduct(repository, None, None, FixedClock()).execute(
                UpdateProductCommand(
                    product_id=1,
                    changes={"provider": 2},
                    updated_by=ACTOR,
                )
            )

        self.assertEqual(raised.exception.field_name, "provider")
        self.assertEqual(repository.product.provider, 1)

    def test_patch_can_repeat_same_provider_without_changing_it(self):
        repository = FakeProductRepository(product_entity())

        result = UpdateProduct(repository, None, None, FixedClock()).execute(
            UpdateProductCommand(
                product_id=1,
                changes={"provider": 1},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(result.provider, 1)
        self.assertIn("PATCH: sin cambios", repository.product.log)
        self.assertEqual(result.version, 1)

    def test_delete_is_soft_and_records_audit_log(self):
        repository = FakeProductRepository(product_entity())
        command = DeleteProductCommand(product_id=1, deleted_by=ACTOR)

        result = DeleteProduct(repository, FixedClock()).execute(command)

        self.assertFalse(result.is_active)
        self.assertTrue(result.is_deleted)
        self.assertEqual(
            repository.product.log,
            f"init; DELETE: 2026-07-15 17:23:13.339 (USER: {ACTOR});",
        )

    def test_patch_confirmation_sets_audit_from_updated_by(self):
        repository = FakeProductRepository(product_entity())
        command = UpdateProductCommand(
            product_id=1,
            changes={"is_confirmed": True},
            updated_by=ACTOR,
        )

        result = UpdateProduct(repository, None, None, FixedClock()).execute(command)

        self.assertTrue(result.is_confirmed)
        self.assertEqual(result.version, 2)
        self.assertEqual(result.confirmed_at, NOW)
        self.assertEqual(result.confirmed_by, ACTOR)
        self.assertEqual(
            repository.product.log,
            f"init; PATCH: is_confirmed=True (USER: {ACTOR});",
        )

    def test_patch_confirmation_repairs_missing_audit(self):
        product = product_entity()
        product.is_confirmed = True
        repository = FakeProductRepository(product)

        result = UpdateProduct(repository, None, None, FixedClock()).execute(
            UpdateProductCommand(
                product_id=1,
                changes={"is_confirmed": True},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(result.confirmed_at, NOW)
        self.assertEqual(result.confirmed_by, ACTOR)
        self.assertIn("PATCH: is_confirmed=True", repository.product.log)

    def test_patch_unconfirmation_clears_audit_fields(self):
        product = product_entity()
        product.is_confirmed = True
        product.confirmed_at = NOW
        product.confirmed_by = ACTOR
        repository = FakeProductRepository(product)

        result = UpdateProduct(repository, None, None, FixedClock()).execute(
            UpdateProductCommand(
                product_id=1,
                changes={"is_confirmed": False},
                updated_by=ACTOR,
            )
        )

        self.assertFalse(result.is_confirmed)
        self.assertIsNone(result.confirmed_at)
        self.assertIsNone(result.confirmed_by)
        self.assertIn("PATCH: is_confirmed=False", repository.product.log)

    def test_second_confirmation_preserves_original_audit(self):
        original_confirmation = datetime(
            2026,
            7,
            14,
            12,
            0,
            tzinfo=timezone.utc,
        )
        product = product_entity()
        product.is_confirmed = True
        product.confirmed_at = original_confirmation
        product.confirmed_by = ACTOR
        repository = FakeProductRepository(product)

        result = UpdateProduct(repository, None, None, FixedClock()).execute(
            UpdateProductCommand(
                product_id=1,
                changes={"is_confirmed": True},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(result.confirmed_at, original_confirmation)
        self.assertEqual(result.confirmed_by, ACTOR)
        self.assertIn("PATCH: sin cambios", repository.product.log)
