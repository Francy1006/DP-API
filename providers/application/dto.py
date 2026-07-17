from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from providers.domain.entities import Provider


@dataclass(frozen=True)
class ProviderDTO:
    id: Optional[int]
    code: str
    provider: str
    type: int
    type_name: Optional[str]
    rating: int
    obs_provider: str
    contact_name: Optional[str]
    contact_mail: Optional[str]
    contact_phone: Optional[int]
    contact_phone2: Optional[int]
    website_url: Optional[str]
    obs_contact: Optional[str]
    company_name: Optional[str]
    company_rut: Optional[str]
    company_activity: Optional[str]
    legal_representative: Optional[str]
    billing_address: Optional[str]
    billing_mail: Optional[str]
    billing_phone: Optional[int]
    company_bank: Optional[int]
    bank_name: Optional[str]
    bank_account_type: Optional[int]
    bank_account_type_name: Optional[str]
    bank_account_number: Optional[str]
    bank_account_mail: Optional[str]
    dispatch_address: Optional[str]
    dispatch_maps_location: Optional[str]
    obs_dispatch: Optional[str]
    dispatch_district: Optional[int]
    dispatch_district_name: Optional[str]
    dispatch_region: Optional[int]
    dispatch_region_name: Optional[str]
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
    log: str
    version: int

    @classmethod
    def from_entity(cls, provider: Provider) -> "ProviderDTO":
        return cls(**asdict(provider))
