from datetime import datetime
from typing import Optional, Protocol, Sequence

from pricing.domain.entities import Price, PriceComponents, PriceConfiguration

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


class PriceRepository(Protocol):
    def get_for_update(self, price_code: str) -> Price: ...

    def count_product_references(self, price_code: str) -> int: ...

    def get_product_configuration(
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
        product_code: str,
        created_at: datetime,
        created_by: str,
    ) -> Price: ...

    def deactivate(self, price_code: str) -> None: ...
