from providers.application.commands import ListProvidersQuery
from providers.application.dto import ProviderDTO
from providers.domain.repositories import ProviderRepository


class ListProviders:
    def __init__(self, repository: ProviderRepository):
        self.repository = repository

    def execute(self, query: ListProvidersQuery) -> list[ProviderDTO]:
        providers = self.repository.list(
            filters=query.filters,
            search=query.search,
            ordering=query.ordering,
        )
        return [ProviderDTO.from_entity(provider) for provider in providers]
