from decimal import Decimal

from products.domain.entities import Product


DEFAULT_ACTOR = "5fbf2886-4ad0-11f0-8ce6-0242ac120002"
DEFAULT_CONFIGURATION = "cd746343-baf4-4359-b2e6-9bd829631e30"


def build_product(**overrides):
    """Build a deterministic Product domain entity without database access."""

    values = {
        "id": 1,
        "code": "3facdae4-c44e-475c-9911-d11b5fdf9980",
        "sku": "PRODUCTO-TEST",
        "description": "PRODUCTO DE VALIDACIÓN API",
        "obs": "REGISTRO TEMPORAL",
        "package_unit": 1,
        "min_package_purchase": 1,
        "price": "bf397d95-c18c-4620-88c9-af621f553951",
        "provider": 1,
        "type": 1,
        "item_group": 6,
        "category": 8,
        "package": 1,
        "created_by": DEFAULT_ACTOR,
        "base_net_amount": Decimal("16980"),
        "net_amount": Decimal("16980"),
        "gross_amount": Decimal("20206.20"),
        "iva_amount": Decimal("3226.20"),
        "aditional_tax_amount": Decimal("0"),
        "retention_amount": Decimal("0"),
        "price_configuration": DEFAULT_CONFIGURATION,
        "price_configuration_label": "PRODUCT_NORMAL_IVA",
        "provider_name": "PROVEEDOR DE PRUEBA",
        "type_name": "PRODUCTO",
        "item_group_name": "GRUPO DE PRUEBA",
        "category_name": "CATEGORÍA DE PRUEBA",
        "package_description": "PAQUETE DE PRUEBA",
        "log": "init;",
    }
    values.update(overrides)
    return Product(**values)
