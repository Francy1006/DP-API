from datetime import datetime
from typing import Optional, Protocol, Sequence

from pricing.domain.entities import Price, PriceComponents, PriceConfiguration

from .entities import Material


class MaterialRepository(Protocol):
    def get(self, material_id: int) -> Material: ...

    def get_for_update(self, material_id: int) -> Material: ...

    def list(
        self,
        filters: dict[str, object],
        search: Optional[str],
        ordering: Sequence[str],
        active_only: bool = False,
    ) -> Sequence[Material]: ...

    def create(self, material: Material) -> Material: ...

    def update(self, material: Material, changed_fields: set[str]) -> Material: ...

    def soft_delete(self, material: Material) -> Material: ...

    def user_exists(self, user_code: str) -> bool: ...


class MaterialClock(Protocol):
    def now(self) -> datetime: ...

    def format_log_timestamp(self, value: datetime) -> str: ...


class MaterialPriceRepository(Protocol):
    def get_for_update(self, price_code: str) -> Price: ...

    def count_material_references(self, price_code: str) -> int: ...

    def get_material_configuration(
        self,
        configuration_code: str,
    ) -> PriceConfiguration: ...

    def get_formula_variables(
        self,
        configuration_code: str,
    ) -> dict[str, object]: ...

    def create_version(
        self,
        components: PriceComponents,
        configuration_code: str,
        material_code: str,
        created_at: datetime,
        created_by: str,
    ) -> Price: ...

    def deactivate(self, price_code: str) -> None: ...
