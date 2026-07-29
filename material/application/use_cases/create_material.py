from material.application.calculate_price import CalculateMaterialPrice
from material.application.commands import CreateMaterialCommand
from material.application.dto import MaterialDTO
from material.domain.entities import Material
from material.domain.exceptions import (
    MaterialAuditUserNotFound,
    MaterialAuditUserRequired,
)
from material.domain.repositories import (
    MaterialClock,
    MaterialPriceRepository,
    MaterialRepository,
)
from pricing.domain.repositories import TransactionManager


class CreateMaterial:
    def __init__(
        self,
        repository: MaterialRepository,
        price_repository: MaterialPriceRepository,
        transaction_manager: TransactionManager,
        clock: MaterialClock,
    ):
        self.repository = repository
        self.price_repository = price_repository
        self.transaction_manager = transaction_manager
        self.clock = clock

    def execute(self, command: CreateMaterialCommand) -> MaterialDTO:
        if not command.created_by:
            raise MaterialAuditUserRequired("created_by")
        if not self.repository.user_exists(command.created_by):
            raise MaterialAuditUserNotFound("created_by")

        values = dict(command.__dict__)
        base_net_amount = values.pop("base_net_amount")
        price_configuration = values.pop("price_configuration")
        material = Material(
            **values,
            price=None,
            base_net_amount=base_net_amount,
            price_configuration=price_configuration,
        )
        material.sku = None
        material.is_confirmed = bool(command.is_confirmed)
        now = self.clock.now()
        material.initialize_audit(now, self.clock.format_log_timestamp(now))

        with self.transaction_manager.atomic():
            calculated = CalculateMaterialPrice(self.price_repository).execute(
                base_net_amount,
                price_configuration,
            )
            price = self.price_repository.create_version(
                components=calculated.components,
                configuration_code=calculated.configuration.code,
                material_code=material.code,
                created_at=now,
                created_by=command.created_by,
            )
            material.link_price(
                price.code,
                calculated.configuration.code,
                calculated.components,
            )
            return MaterialDTO.from_entity(self.repository.create(material))
