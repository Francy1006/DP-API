from typing import Optional, Protocol, Sequence

from .entities import Provider


class ProviderRepository(Protocol):
    def get(self, provider_id: int) -> Provider: ...

    def list(
        self,
        filters: dict[str, object],
        search: Optional[str],
        ordering: Sequence[str],
    ) -> Sequence[Provider]: ...

    def create(self, provider: Provider) -> Provider: ...

    def update(
        self,
        provider: Provider,
        changed_fields: set[str],
    ) -> Provider: ...

    def delete(self, provider_id: int) -> None: ...
