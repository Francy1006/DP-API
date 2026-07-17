from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class CreateProductCommand:
    code: str
    sku: str
    description: str
    obs: str
    package_unit: int
    min_package_purchase: int
    price: str
    provider: int
    type: int
    item_group: int
    category: int
    package: int
    created_by: str
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
