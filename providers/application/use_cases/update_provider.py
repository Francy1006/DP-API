from providers.application.commands import UpdateProviderCommand
from providers.application.dto import ProviderDTO
from providers.domain.repositories import ProviderRepository


class UpdateProvider:
    def __init__(self, repository: ProviderRepository):
        self.repository = repository

    def execute(self, command: UpdateProviderCommand) -> ProviderDTO:
        provider = self.repository.get(command.provider_id)
        provider.apply_changes(command.changes)
        return ProviderDTO.from_entity(
            self.repository.update(provider, set(command.changes))
        )
