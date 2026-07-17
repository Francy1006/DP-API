from providers.application.commands import CreateProviderCommand
from providers.application.dto import ProviderDTO
from providers.domain.entities import Provider
from providers.domain.repositories import ProviderRepository


class CreateProvider:
    def __init__(self, repository: ProviderRepository):
        self.repository = repository

    def execute(self, command: CreateProviderCommand) -> ProviderDTO:
        provider = Provider(**command.data)
        return ProviderDTO.from_entity(self.repository.create(provider))
