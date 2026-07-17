from providers.application.dto import ProviderDTO
from providers.domain.repositories import ProviderRepository


class GetProvider:
    def __init__(self, repository: ProviderRepository):
        self.repository = repository

    def execute(self, provider_id: int) -> ProviderDTO:
        return ProviderDTO.from_entity(self.repository.get(provider_id))
