from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class Provider:
    code: str
    provider: str
    type: int
    rating: int
    obs_provider: str
    created_by: str
    id: Optional[int] = None
    type_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_mail: Optional[str] = None
    contact_phone: Optional[int] = None
    contact_phone2: Optional[int] = None
    website_url: Optional[str] = None
    obs_contact: Optional[str] = None
    company_name: Optional[str] = None
    company_rut: Optional[str] = None
    company_activity: Optional[str] = None
    legal_representative: Optional[str] = None
    billing_address: Optional[str] = None
    billing_mail: Optional[str] = None
    billing_phone: Optional[int] = None
    company_bank: Optional[int] = None
    bank_name: Optional[str] = None
    bank_account_type: Optional[int] = None
    bank_account_type_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_account_mail: Optional[str] = None
    dispatch_address: Optional[str] = None
    dispatch_maps_location: Optional[str] = None
    obs_dispatch: Optional[str] = None
    dispatch_district: Optional[int] = None
    dispatch_district_name: Optional[str] = None
    dispatch_region: Optional[int] = None
    dispatch_region_name: Optional[str] = None
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

    def apply_changes(self, changes: dict[str, Any]) -> None:
        for field_name, value in changes.items():
            setattr(self, field_name, value)
