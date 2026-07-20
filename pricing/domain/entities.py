from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Price:
    code: str
    base_net_amount: Decimal
    net_amount: Decimal
    gross_amount: Decimal
    iva_amount: Decimal
    aditional_tax_amount: Decimal
    retention_amount: Decimal
    price_configuration: str
    is_current: Optional[bool]
    is_deleted: Optional[bool]
    is_confirmed: Optional[bool]
    created_at: Optional[datetime]
    created_by: str
    record_item_code: Optional[str]
    price_record_type: Optional[int]


@dataclass(frozen=True)
class ProductPriceConfiguration:
    code: str
    name: str
    record_type: int
    variable_formula_code: str
    variable_formula_name: str
    formula_template: str


@dataclass(frozen=True)
class PriceComponents:
    gross_amount: Decimal
    base_net_amount: Decimal
    net_amount: Decimal
    iva_amount: Decimal
    aditional_tax_amount: Decimal = Decimal("0.00")
    retention_amount: Decimal = Decimal("0.00")
