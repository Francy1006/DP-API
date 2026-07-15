from products.application.commands import UpdateProductCommand
from products.application.dto import ProductDTO
from products.domain.exceptions import AuditUserNotFound, AuditUserRequired
from products.domain.repositories import Clock, ProductRepository


class UpdateProduct:
    def __init__(self, repository: ProductRepository, clock: Clock):
        self.repository = repository
        self.clock = clock

    def execute(self, command: UpdateProductCommand) -> ProductDTO:
        if not command.updated_by:
            raise AuditUserRequired("updated_by")
        if not self.repository.user_exists(command.updated_by):
            raise AuditUserNotFound("updated_by")

        product = self.repository.get(command.product_id)
        product.apply_patch(command.changes, command.updated_by, self.clock.now())
        changed_fields = set(command.changes) | {"updated_by", "updated_at", "log"}
        return ProductDTO.from_entity(
            self.repository.update(product, changed_fields)
        )
