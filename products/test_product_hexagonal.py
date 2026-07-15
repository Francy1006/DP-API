from datetime import datetime, timezone

from django.test import SimpleTestCase
from django.urls import reverse

from products.application.commands import (
    CreateProductCommand,
    DeleteProductCommand,
    UpdateProductCommand,
)
from products.application.use_cases import CreateProduct, DeleteProduct, UpdateProduct
from products.domain.entities import Product
from products.presentation.serializers import ProductSerializer
from products.presentation.views import ProductViewSet


ACTOR = "5fbf2886-4ad0-11f0-8ce6-0242ac120002"
NOW = datetime(2026, 7, 15, 17, 23, 13, 339000, tzinfo=timezone.utc)


class FixedClock:
    def now(self):
        return NOW

    def format_log_timestamp(self, value):
        return "2026-07-15 17:23:13.339"


class FakeProductRepository:
    def __init__(self, product=None):
        self.product = product

    def get(self, product_id):
        return self.product

    def list(self, filters, search, ordering, active_only=False):
        return [self.product] if self.product else []

    def create(self, product):
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
        "price_gross_amount",
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
        self.assertEqual(
            ProductViewSet.http_method_names,
            ["get", "post", "patch", "head", "options"],
        )

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
            price="bf397d95-c18c-4620-88c9-af621f553951",
            provider=1,
            type=1,
            item_group=6,
            category=8,
            package=1,
            created_by=ACTOR,
        )

        result = CreateProduct(repository, FixedClock()).execute(command)

        self.assertEqual(result.id, 1)
        self.assertEqual(repository.product.created_at, NOW)
        self.assertEqual(
            repository.product.log,
            f"INIT: 2026-07-15 17:23:13.339 (USER: {ACTOR});",
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

        UpdateProduct(repository, FixedClock()).execute(command)

        self.assertEqual(
            repository.product.log,
            "init; PATCH: description='descripción actualizada', "
            f"obs='observaciones actualizada' (USER: {ACTOR});",
        )
        self.assertTrue(repository.product.log.endswith(";"))

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
