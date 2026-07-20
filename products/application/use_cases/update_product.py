from products.application.commands import UpdateProductCommand
from products.application.dto import ProductDTO
from products.domain.exceptions import AuditUserNotFound, AuditUserRequired
from products.domain.repositories import Clock, ProductRepository
from pricing.application import CalculateProductPrice
from pricing.domain.exceptions import UnsafeCurrentPrice
from pricing.domain.repositories import PriceRepository, TransactionManager


class UpdateProduct:
    def __init__(
        self,
        repository: ProductRepository,
        price_repository: PriceRepository,
        transaction_manager: TransactionManager,
        clock: Clock,
    ):
        self.repository = repository
        self.price_repository = price_repository
        self.transaction_manager = transaction_manager
        self.clock = clock

    def execute(self, command: UpdateProductCommand) -> ProductDTO:
        if not command.updated_by:
            raise AuditUserRequired("updated_by")
        if not self.repository.user_exists(command.updated_by):
            raise AuditUserNotFound("updated_by")

        changes = dict(command.changes)
        pricing_change_requested = bool(
            {"base_net_amount", "price_configuration"}.intersection(changes)
        )
        if not pricing_change_requested:
            product = self.repository.get(command.product_id)
            modified = product.apply_patch(
                changes,
                command.updated_by,
                self.clock.now(),
            )
            if modified:
                product.increment_version()
            return ProductDTO.from_entity(
                self.repository.update(
                    product,
                    self._changed_product_fields(changes, modified),
                )
            )

        with self.transaction_manager.atomic():
            product = self.repository.get_for_update(command.product_id)
            current_price = self.price_repository.get_for_update(product.price)
            if current_price.is_current is not True or current_price.is_deleted is True:
                raise UnsafeCurrentPrice(
                    "The Product does not reference an active current Price"
                )

            requested_base_net = changes.get(
                "base_net_amount",
                current_price.base_net_amount,
            )
            requested_configuration = changes.get(
                "price_configuration",
                current_price.price_configuration,
            )
            calculated = CalculateProductPrice(self.price_repository).execute(
                requested_base_net,
                requested_configuration,
            )
            now = self.clock.now()
            modified = product.apply_patch(changes, command.updated_by, now)

            if self._same_persisted_price(
                current_price,
                calculated.configuration.code,
                calculated.components,
            ):
                if modified:
                    product.increment_version()
                return ProductDTO.from_entity(
                    self.repository.update(
                        product,
                        self._changed_product_fields(
                            self._normal_product_changes(changes),
                            modified,
                        ),
                    )
                )

            owns_current_price_exclusively = (
                current_price.record_item_code == product.code
                and current_price.price_record_type == 1
                and self.price_repository.count_product_references(
                    current_price.code
                )
                == 1
            )

            new_price = self.price_repository.create_version(
                components=calculated.components,
                configuration_code=calculated.configuration.code,
                product_code=product.code,
                created_at=now,
                created_by=command.updated_by,
            )
            # A shared or inconsistently owned legacy Price must remain current
            # for its other consumers. Fork a Product-owned version and only
            # deactivate the previous row when this Product is its sole owner.
            if owns_current_price_exclusively:
                self.price_repository.deactivate(current_price.code)
            product.link_price(
                new_price.code,
                calculated.configuration.code,
                calculated.components,
            )
            product.increment_version()

            changed_fields = self._changed_product_fields(
                self._normal_product_changes(changes),
                True,
            ) | {"price"}
            return ProductDTO.from_entity(
                self.repository.update(product, changed_fields)
            )

    @staticmethod
    def _changed_product_fields(changes, include_version=False):
        changed_fields = set(changes) | {"updated_by", "updated_at", "log"}
        if "is_confirmed" in changes:
            changed_fields.update({"confirmed_at", "confirmed_by"})
        if include_version:
            changed_fields.add("version")
        return changed_fields

    @staticmethod
    def _normal_product_changes(changes):
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
