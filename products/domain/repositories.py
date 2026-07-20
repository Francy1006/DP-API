from datetime import datetime
from typing import Optional, Protocol, Sequence

from .entities import Product


class ProductRepository(Protocol):
    def get(self, product_id: int) -> Product: ...

    def get_for_update(self, product_id: int) -> Product: ...

    def list(
        self,
        filters: dict[str, object],
        search: Optional[str],
        ordering: Sequence[str],
        active_only: bool = False,
    ) -> Sequence[Product]: ...

    def create(self, product: Product) -> Product: ...

    def update(self, product: Product, changed_fields: set[str]) -> Product: ...

    def soft_delete(self, product: Product) -> Product: ...

    def user_exists(self, user_code: str) -> bool: ...


class Clock(Protocol):
    def now(self) -> datetime: ...

    def format_log_timestamp(self, value: datetime) -> str: ...
