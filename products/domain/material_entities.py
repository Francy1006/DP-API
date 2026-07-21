from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from .material_exceptions import ImmutableMaterialField


def _terminated_log(value: str) -> str:
    current = (value or "").strip()
    if current and not current.endswith(";"):
        current = f"{current};"
    return current


def _audit_value(value) -> str:
    if isinstance(value, Decimal):
        return format(value, "f")
    return repr(value)


@dataclass
class Material:
    """Material aggregate without Django or REST dependencies."""

    code: str
    description: str
    obs: str
    package_unit: int
    min_package_purchase: int
    price: Optional[str]
    provider: int
    type: int
    item_group: int
    category: int
    package: int
    created_by: str
    sku: Optional[str] = None
    id: Optional[int] = None
    base_net_amount: Optional[Decimal] = None
    net_amount: Optional[Decimal] = None
    gross_amount: Optional[Decimal] = None
    iva_amount: Optional[Decimal] = None
    aditional_tax_amount: Optional[Decimal] = None
    retention_amount: Optional[Decimal] = None
    price_configuration: Optional[str] = None
    price_configuration_label: Optional[str] = None
    provider_name: Optional[str] = None
    type_name: Optional[str] = None
    item_group_name: Optional[str] = None
    category_name: Optional[str] = None
    package_description: Optional[str] = None
    url: Optional[str] = None
    is_active: bool = True
    is_deleted: Optional[bool] = None
    is_confirmed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    confirmed_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None
    log: str = "init;"
    version: int = 1

    def initialize_audit(self, created_at: datetime, timestamp: str) -> None:
        self.created_at = created_at
        if self.is_confirmed:
            self.confirmed_at = created_at
            self.confirmed_by = self.created_by
            self.log = (
                f"INIT: {timestamp} (USER: {self.created_by}) (confirmed);"
            )
        else:
            self.is_confirmed = False
            self.confirmed_at = None
            self.confirmed_by = None
            self.log = f"INIT: {timestamp} (USER: {self.created_by});"

    def apply_patch(
        self,
        changes: dict[str, Any],
        updated_by: str,
        updated_at: datetime,
    ) -> bool:
        changed_values = []
        for field_name, new_value in changes.items():
            if field_name in {"sku", "provider", "price", "code"}:
                if getattr(self, field_name) != new_value:
                    raise ImmutableMaterialField(field_name)
                continue

            if field_name == "is_confirmed":
                normalized_value = bool(new_value)
                was_confirmed = self.is_confirmed is True
                audit_incomplete = normalized_value and (
                    self.confirmed_at is None or self.confirmed_by is None
                )
                stale_audit = not normalized_value and (
                    self.confirmed_at is not None or self.confirmed_by is not None
                )
                if (
                    self.is_confirmed != normalized_value
                    or audit_incomplete
                    or stale_audit
                ):
                    changed_values.append(
                        f"is_confirmed={normalized_value!r}"
                    )

                self.is_confirmed = normalized_value
                if normalized_value:
                    if not was_confirmed or audit_incomplete:
                        self.confirmed_at = updated_at
                        self.confirmed_by = updated_by
                else:
                    self.confirmed_at = None
                    self.confirmed_by = None
                continue

            if getattr(self, field_name) != new_value:
                changed_values.append(
                    f"{field_name}={_audit_value(new_value)}"
                )
                setattr(self, field_name, new_value)

        changes_log = ", ".join(changed_values) if changed_values else "sin cambios"
        current_log = _terminated_log(self.log)
        patch_log = f"PATCH: {changes_log} (USER: {updated_by});"
        self.log = f"{current_log} {patch_log}".strip()
        self.updated_by = updated_by
        self.updated_at = updated_at
        return bool(changed_values)

    def link_price(self, price_code, configuration_code, components) -> None:
        self.price = price_code
        self.price_configuration = configuration_code
        self.base_net_amount = components.base_net_amount
        self.net_amount = components.net_amount
        self.gross_amount = components.gross_amount
        self.iva_amount = components.iva_amount
        self.aditional_tax_amount = components.aditional_tax_amount
        self.retention_amount = components.retention_amount

    def increment_version(self) -> None:
        self.version = (self.version or 0) + 1

    def soft_delete(
        self,
        deleted_by: str,
        deleted_at: datetime,
        timestamp: str,
    ) -> None:
        current_log = _terminated_log(self.log)
        delete_log = f"DELETE: {timestamp} (USER: {deleted_by});"
        self.log = f"{current_log} {delete_log}".strip()
        self.is_active = False
        self.is_deleted = True
        self.deleted_by = deleted_by
        self.deleted_at = deleted_at
