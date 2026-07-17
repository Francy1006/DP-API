from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class CreateProviderCommand:
    data: dict[str, Any]


@dataclass(frozen=True)
class UpdateProviderCommand:
    provider_id: int
    changes: dict[str, Any]


@dataclass(frozen=True)
class ListProvidersQuery:
    filters: dict[str, object] = field(default_factory=dict)
    search: Optional[str] = None
    ordering: tuple[str, ...] = ("provider",)
