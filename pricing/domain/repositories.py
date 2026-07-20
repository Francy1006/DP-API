from datetime import datetime
from contextlib import AbstractContextManager
from typing import Protocol

from .entities import (
    Price,
    PriceComponents,
    ProductPriceConfiguration,
)


class PriceRepository(Protocol):
    def get_for_update(self, price_code: str) -> Price: ...

    def count_product_references(self, price_code: str) -> int: ...

    def get_product_configuration(
        self,
        configuration_code: str,
    ) -> ProductPriceConfiguration: ...

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


class TransactionManager(Protocol):
    def atomic(self) -> AbstractContextManager: ...
