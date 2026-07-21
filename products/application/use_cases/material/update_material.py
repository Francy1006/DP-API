from products.application.material_commands import UpdateMaterialCommand
from products.application.material_dto import MaterialDTO
from products.domain.material_exceptions import (
    LegacyMaterialPriceInputRequired,
    MaterialAuditUserNotFound,
    MaterialAuditUserRequired,
)
from products.domain.material_repositories import MaterialClock, MaterialRepository
from pricing.application import CalculateMaterialPrice
from pricing.domain.exceptions import CurrentPriceNotFound, UnsafeCurrentPrice
from pricing.domain.repositories import MaterialPriceRepository, TransactionManager


class UpdateMaterial:
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

    def execute(self, command: UpdateMaterialCommand) -> MaterialDTO:
        if not command.updated_by:
            raise MaterialAuditUserRequired("updated_by")
        if not self.repository.user_exists(command.updated_by):
            raise MaterialAuditUserNotFound("updated_by")

        changes = dict(command.changes)
        pricing_change_requested = bool(
            {"base_net_amount", "price_configuration"}.intersection(changes)
        )
        if not pricing_change_requested:
            material = self.repository.get(command.material_id)
            modified = material.apply_patch(
                changes,
                command.updated_by,
                self.clock.now(),
            )
            if modified:
                material.increment_version()
            return MaterialDTO.from_entity(
                self.repository.update(
                    material,
                    self._changed_material_fields(changes, modified),
                )
            )

        with self.transaction_manager.atomic():
            material = self.repository.get_for_update(command.material_id)
            try:
                current_price = self.price_repository.get_for_update(material.price)
            except CurrentPriceNotFound:
                current_price = None

            requested_base_net = changes.get(
                "base_net_amount",
                current_price.base_net_amount if current_price else None,
            )
            requested_configuration = changes.get(
                "price_configuration",
                current_price.price_configuration if current_price else None,
            )
            missing_fields = []
            if requested_base_net is None:
                missing_fields.append("base_net_amount")
            if not requested_configuration:
                missing_fields.append("price_configuration")
            if missing_fields:
                raise LegacyMaterialPriceInputRequired(missing_fields)

            if current_price and (
                current_price.is_current is not True
                or current_price.is_deleted is True
            ):
                raise UnsafeCurrentPrice(
                    "The Material does not reference an active current Price"
                )

            calculated = CalculateMaterialPrice(self.price_repository).execute(
                requested_base_net,
                requested_configuration,
            )
            now = self.clock.now()
            modified = material.apply_patch(changes, command.updated_by, now)

            if current_price and self._same_persisted_price(
                current_price,
                calculated.configuration.code,
                calculated.components,
            ):
                if modified:
                    material.increment_version()
                return MaterialDTO.from_entity(
                    self.repository.update(
                        material,
                        self._changed_material_fields(
                            self._normal_material_changes(changes),
                            modified,
                        ),
                    )
                )

            owns_current_price_exclusively = bool(
                current_price
                and current_price.record_item_code == material.code
                and current_price.price_record_type == 2
                and self.price_repository.count_material_references(
                    current_price.code
                )
                == 1
            )

            new_price = self.price_repository.create_version(
                components=calculated.components,
                configuration_code=calculated.configuration.code,
                product_code=material.code,
                created_at=now,
                created_by=command.updated_by,
            )
            if owns_current_price_exclusively:
                self.price_repository.deactivate(current_price.code)
            material.link_price(
                new_price.code,
                calculated.configuration.code,
                calculated.components,
            )
            material.increment_version()

            changed_fields = self._changed_material_fields(
                self._normal_material_changes(changes),
                True,
            ) | {"price"}
            return MaterialDTO.from_entity(
                self.repository.update(material, changed_fields)
            )

    @staticmethod
    def _changed_material_fields(changes, include_version=False):
        changed_fields = set(changes) | {"updated_by", "updated_at", "log"}
        if "is_confirmed" in changes:
            changed_fields.update({"confirmed_at", "confirmed_by"})
        if include_version:
            changed_fields.add("version")
        return changed_fields

    @staticmethod
    def _normal_material_changes(changes):
        return {
            field_name: value
            for field_name, value in changes.items()
            if field_name not in {"base_net_amount", "price_configuration"}
        }

    @staticmethod
    def _same_persisted_price(current_price, configuration_code, components):
        return (
            current_price.price_configuration == configuration_code
            and current_price.base_net_amount == components.base_net_amount
            and current_price.net_amount == components.net_amount
            and current_price.gross_amount == components.gross_amount
            and current_price.iva_amount == components.iva_amount
            and current_price.aditional_tax_amount
            == components.aditional_tax_amount
            and current_price.retention_amount == components.retention_amount
        )
