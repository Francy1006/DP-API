from datetime import datetime
from typing import Optional, Protocol, Sequence

from .material_entities import Material


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
