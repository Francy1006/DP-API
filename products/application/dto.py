from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from products.domain.entities import Product


@dataclass(frozen=True)
class ProductDTO:
    id: Optional[int]
    code: str
    sku: Optional[str]
    description: str
    obs: str
    package_unit: int
    min_package_purchase: int
    price: Optional[str]
    base_net_amount: Optional[Decimal]
    net_amount: Optional[Decimal]
    gross_amount: Optional[Decimal]
    iva_amount: Optional[Decimal]
    aditional_tax_amount: Optional[Decimal]
    retention_amount: Optional[Decimal]
    price_configuration: Optional[str]
    price_configuration_label: Optional[str]
    provider: int
    provider_name: Optional[str]
    type: int
    type_name: Optional[str]
    item_group: int
    item_group_name: Optional[str]
    category: int
    category_name: Optional[str]
    url: Optional[str]
    package: int
    package_description: Optional[str]
    is_active: bool
    is_deleted: Optional[bool]
    is_confirmed: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    confirmed_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_by: str
    confirmed_by: Optional[str]
    updated_by: Optional[str]
    deleted_by: Optional[str]
    version: int

    @classmethod
    def from_entity(cls, product: Product) -> "ProductDTO":
        values = asdict(product)
        values.pop("log", None)
        return cls(**values)


@dataclass(frozen=True)
class DeletedProductDTO:
    id: int
    is_active: bool
    is_deleted: bool
    deleted_at: datetime
    deleted_by: str

    @classmethod
    def from_entity(cls, product: Product) -> "DeletedProductDTO":
        return cls(
            id=product.id,
            is_active=product.is_active,
            is_deleted=product.is_deleted,
            deleted_at=product.deleted_at,
            deleted_by=product.deleted_by,
        )
