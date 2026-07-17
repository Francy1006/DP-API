from providers.domain.repositories import ProviderRepository


class DeleteProvider:
    def __init__(self, repository: ProviderRepository):
        self.repository = repository

    def execute(self, provider_id: int) -> None:
        self.repository.delete(provider_id)
