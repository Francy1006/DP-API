from contextlib import nullcontext
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest

from pricing.domain.entities import Price, ProductPriceConfiguration
from products.domain.exceptions import ProductNotFound
from products.presentation import views as product_views
from products.presentation.views import ProductViewSet
from products.tests.factories import (
    DEFAULT_ACTOR,
    DEFAULT_CONFIGURATION,
    build_product,
)


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


class FixedClock:
    def now(self):
        return NOW

    def format_log_timestamp(self, value):
        return "2026-07-21 08:00:00.000"


class InMemoryProductRepository:
    def __init__(self, product=None):
        self.product = product
        self.physical_rows = {product.id: product} if product else {}
        self.last_filters = None

    def get(self, product_id):
        product = self.physical_rows.get(int(product_id))
        if product is None or product.is_deleted is True:
            raise ProductNotFound
        return product

    def get_for_update(self, product_id):
        return self.get(product_id)

    def list(self, filters, search, ordering, active_only=False):
        self.last_filters = filters
        products = [
            product
            for product in self.physical_rows.values()
            if product.is_deleted is not True
        ]
        if active_only:
            products = [product for product in products if product.is_active]
        for field_name, expected in filters.items():
            products = [
                product
                for product in products
                if getattr(product, field_name) == expected
            ]
        if search:
            normalized = search.lower()
            products = [
                product
                for product in products
                if normalized in product.description.lower()
                or normalized in product.code.lower()
                or normalized in (product.sku or "").lower()
            ]
        return products

    def create(self, product):
        product.id = max(self.physical_rows, default=0) + 1
        product.sku = "P-001-0001"
        product.provider_name = "PROVEEDOR DE PRUEBA"
        product.type_name = "PRODUCTO"
        product.item_group_name = "GRUPO DE PRUEBA"
        product.category_name = "CATEGORÍA DE PRUEBA"
        product.package_description = "PAQUETE DE PRUEBA"
        product.price_configuration_label = "PRODUCT_NORMAL_IVA"
        self.product = product
        self.physical_rows[product.id] = product
        return product

    def update(self, product, changed_fields):
        self.product = product
        self.physical_rows[product.id] = product
        return product

    def soft_delete(self, product):
        self.product = product
        self.physical_rows[product.id] = product
        return product

    def user_exists(self, user_code):
        return user_code == DEFAULT_ACTOR


class InMemoryPriceRepository:
    def __init__(self):
        product = build_product()
        self.current = Price(
            code=product.price,
            base_net_amount=product.base_net_amount,
            net_amount=product.net_amount,
            gross_amount=product.gross_amount,
            iva_amount=product.iva_amount,
            aditional_tax_amount=product.aditional_tax_amount,
            retention_amount=product.retention_amount,
            price_configuration=product.price_configuration,
            is_current=True,
            is_deleted=False,
            is_confirmed=True,
            created_at=NOW,
            created_by=DEFAULT_ACTOR,
            record_item_code=product.code,
            price_record_type=1,
        )
        self.deactivated = []

    def get_for_update(self, price_code):
        return self.current

    def count_product_references(self, price_code):
        return 1

    def get_product_configuration(self, configuration_code):
        if configuration_code != DEFAULT_CONFIGURATION:
            from pricing.domain.exceptions import (
                ProductPriceConfigurationUnavailable,
            )

            raise ProductPriceConfigurationUnavailable
        return ProductPriceConfiguration(
            code=DEFAULT_CONFIGURATION,
            name="PRODUCT_NORMAL_IVA",
            record_type=1,
            variable_formula_code="formula-code",
            variable_formula_name="PRODUCT_STANDARD",
            formula_template=(
                "net_amount=${net_amount};"
                "iva_amount=${net_amount}*${iva};"
                "gross_amount=${net_amount}*(1+${iva});"
            ),
        )

    def get_formula_variables(self, configuration_code):
        return {"iva": Decimal("0.19")}

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
            is_deleted=False,
            is_confirmed=True,
            created_at=created_at,
            created_by=created_by,
            record_item_code=product_code,
            price_record_type=1,
        )

    def deactivate(self, price_code):
        self.deactivated.append(price_code)


class TransactionManager:
    def atomic(self):
        return nullcontext()


class CommandSerializerStub:
    """Exercise HTTP orchestration while serializer rules stay unit-tested."""

    relation_fields = {"provider", "type", "item_group", "category", "package"}
    audit_fields = {"created_by", "updated_by"}

    def __init__(self, instance=None, data=None, partial=False):
        self.initial_data = dict(data or {})
        self.partial = partial
        self.validated_data = {}
        self.errors = {}

    def is_valid(self, raise_exception=False):
        for field_name, value in self.initial_data.items():
            if field_name in self.relation_fields:
                self.validated_data[field_name] = SimpleNamespace(pk=int(value))
            elif field_name in self.audit_fields:
                self.validated_data[field_name] = SimpleNamespace(code=value)
            elif field_name == "base_net_amount":
                self.validated_data[field_name] = Decimal(str(value))
            else:
                self.validated_data[field_name] = value
        return True


@pytest.fixture
def repository(monkeypatch, product_factory):
    repository = InMemoryProductRepository(product_factory())
    monkeypatch.setattr(ProductViewSet, "get_repository", lambda self: repository)
    monkeypatch.setattr(ProductViewSet, "get_clock", lambda self: FixedClock())
    return repository


@pytest.fixture
def command_dependencies(monkeypatch):
    price_repository = InMemoryPriceRepository()
    monkeypatch.setattr(
        product_views,
        "ProductCommandSerializer",
        CommandSerializerStub,
    )
    monkeypatch.setattr(
        product_views,
        "DjangoPriceRepository",
        lambda: price_repository,
    )
    monkeypatch.setattr(
        product_views,
        "DjangoTransactionManager",
        TransactionManager,
    )
    return price_repository


def create_payload():
    return {
        "code": "new-product-code",
        "description": "PRODUCTO NUEVO",
        "obs": "CREADO POR API",
        "package_unit": 1,
        "min_package_purchase": 1,
        "base_net_amount": "1000.00",
        "price_configuration": DEFAULT_CONFIGURATION,
        "provider": 1,
        "type": 1,
        "item_group": 6,
        "category": 8,
        "package": 1,
        "created_by": DEFAULT_ACTOR,
    }


def test_list_products_returns_200_with_standard_pagination(api_client, repository):
    response = api_client.get("/api/products/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert response.data["results"][0]["item_group"] == 6
    assert response.data["results"][0]["item_group_name"] == "GRUPO DE PRUEBA"
    assert "group" not in response.data["results"][0]
    assert "log" not in response.data["results"][0]


def test_retrieve_visible_product_returns_200(api_client, repository):
    response = api_client.get("/api/products/1/")

    assert response.status_code == 200
    assert response.data["id"] == 1
    assert response.data["provider_name"] == "PROVEEDOR DE PRUEBA"


def test_list_products_applies_canonical_filters(api_client, repository):
    response = api_client.get("/api/products/?item_group=6&is_active=true")

    assert response.status_code == 200
    assert repository.last_filters == {"item_group": 6, "is_active": True}


def test_create_product_with_valid_data_returns_201(
    api_client,
    repository,
    command_dependencies,
):
    repository.physical_rows.clear()

    response = api_client.post("/api/products/", create_payload(), format="json")

    assert response.status_code == 201
    assert response.data["sku"] == "P-001-0001"
    assert response.data["price"] == "new-price-code"
    assert response.data["gross_amount"] == Decimal("1190.00")
    assert response.data["version"] == 1


def test_create_product_with_unavailable_price_configuration_returns_400(
    api_client,
    repository,
    command_dependencies,
):
    payload = create_payload()
    payload["price_configuration"] = "unavailable-configuration"

    response = api_client.post("/api/products/", payload, format="json")

    assert response.status_code == 400
    assert "price_configuration" in response.data


def test_patch_product_with_valid_data_returns_200(
    api_client,
    repository,
    command_dependencies,
):
    response = api_client.patch(
        "/api/products/1/",
        {"description": "DESCRIPCIÓN ACTUALIZADA", "updated_by": DEFAULT_ACTOR},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["description"] == "DESCRIPCIÓN ACTUALIZADA"
    assert response.data["version"] == 2


def test_patch_product_price_creates_new_price_version(
    api_client,
    repository,
    command_dependencies,
):
    previous_price = repository.product.price

    response = api_client.patch(
        "/api/products/1/",
        {"base_net_amount": "2000.00", "updated_by": DEFAULT_ACTOR},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["price"] == "new-price-code"
    assert response.data["base_net_amount"] == Decimal("2000.00")
    assert response.data["gross_amount"] == Decimal("2380.00")
    assert response.data["version"] == 2
    assert command_dependencies.deactivated == [previous_price]


def test_patch_product_with_changed_provider_returns_400(
    api_client,
    repository,
    command_dependencies,
):
    response = api_client.patch(
        "/api/products/1/",
        {"provider": 2, "updated_by": DEFAULT_ACTOR},
        format="json",
    )

    assert response.status_code == 400
    assert "provider" in response.data
    assert repository.product.provider == 1


def test_patch_product_with_same_provider_returns_200(
    api_client,
    repository,
    command_dependencies,
):
    response = api_client.patch(
        "/api/products/1/",
        {"provider": 1, "updated_by": DEFAULT_ACTOR},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["provider"] == 1
    assert response.data["version"] == 1


def test_put_product_returns_405(api_client, repository):
    response = api_client.put("/api/products/1/", {}, format="json")

    assert response.status_code == 405


def test_http_delete_product_returns_405(api_client, repository):
    response = api_client.delete("/api/products/1/")

    assert response.status_code == 405


def test_head_product_list_and_detail_return_200(api_client, repository):
    assert api_client.head("/api/products/").status_code == 200
    assert api_client.head("/api/products/1/").status_code == 200


def test_delete_product_logically_hides_product_from_list_and_detail(
    api_client,
    repository,
):
    response = api_client.post(
        "/api/products/1/delete/",
        {"deleted_by": DEFAULT_ACTOR},
        format="json",
    )

    assert response.status_code == 200
    assert 1 in repository.physical_rows
    stored = repository.physical_rows[1]
    assert stored.is_active is False
    assert stored.is_deleted is True
    assert stored.deleted_at == NOW
    assert stored.deleted_by == DEFAULT_ACTOR
    assert stored.log.endswith(";")
    assert api_client.get("/api/products/").data["count"] == 0
    assert api_client.get("/api/products/1/").status_code == 404
