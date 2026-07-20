from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Optional


@dataclass(frozen=True)
class CreateProductCommand:
    code: str
    description: str
    obs: str
    package_unit: int
    min_package_purchase: int
    base_net_amount: Decimal
    price_configuration: str
    provider: int
    type: int
    item_group: int
    category: int
    package: int
    created_by: str
    sku: Optional[str] = None
    url: Optional[str] = None
    is_active: bool = True
    is_confirmed: Optional[bool] = None
    updated_by: Optional[str] = None


@dataclass(frozen=True)
class UpdateProductCommand:
    product_id: int
    changes: dict[str, Any]
    updated_by: Optional[str]


@dataclass(frozen=True)
class DeleteProductCommand:
    product_id: int
    deleted_by: Optional[str]


@dataclass(frozen=True)
class ListProductsQuery:
    filters: dict[str, object] = field(default_factory=dict)
    search: Optional[str] = None
    ordering: tuple[str, ...] = ("description",)
    active_only: bool = False
