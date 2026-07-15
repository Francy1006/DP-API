from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


def _terminated_log(value: str) -> str:
    current = (value or "").strip()
    if current and not current.endswith(";"):
        current = f"{current};"
    return current


@dataclass
class Product:
    """Product aggregate without Django or persistence dependencies."""

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
    id: Optional[int] = None
    price_gross_amount: Optional[int] = None
    provider_name: Optional[str] = None
    type_name: Optional[str] = None
    item_group_name: Optional[str] = None
    category_name: Optional[str] = None
    package_description: Optional[str] = None
    url: Optional[str] = None
    is_active: bool = True
    is_deleted: Optional[bool] = None
    is_confirmed: Optional[bool] = None
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
        self.log = f"INIT: {timestamp} (USER: {self.created_by});"

    def apply_patch(
        self,
        changes: dict[str, Any],
        updated_by: str,
        updated_at: datetime,
    ) -> None:
        changed_values = []
        for field_name, new_value in changes.items():
            if getattr(self, field_name) != new_value:
                changed_values.append(f"{field_name}={new_value!r}")
                setattr(self, field_name, new_value)

        changes_log = ", ".join(changed_values) if changed_values else "sin cambios"
        patch_log = f"PATCH: {changes_log} (USER: {updated_by});"
        current_log = _terminated_log(self.log)
        self.log = f"{current_log} {patch_log}".strip()
        self.updated_by = updated_by
        self.updated_at = updated_at

    def soft_delete(
        self,
        deleted_by: str,
        deleted_at: datetime,
        timestamp: str,
    ) -> None:
        delete_log = f"DELETE: {timestamp} (USER: {deleted_by});"
        current_log = _terminated_log(self.log)
        self.log = f"{current_log} {delete_log}".strip()
        self.is_active = False
        self.is_deleted = True
        self.deleted_by = deleted_by
        self.deleted_at = deleted_at
