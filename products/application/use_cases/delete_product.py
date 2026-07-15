from products.application.commands import DeleteProductCommand
from products.application.dto import DeletedProductDTO
from products.domain.exceptions import AuditUserNotFound, AuditUserRequired
from products.domain.repositories import Clock, ProductRepository


class DeleteProduct:
    def __init__(self, repository: ProductRepository, clock: Clock):
        self.repository = repository
        self.clock = clock

    def execute(self, command: DeleteProductCommand) -> DeletedProductDTO:
        product = self.repository.get(command.product_id)
        if not command.deleted_by:
            raise AuditUserRequired("deleted_by")
        if not self.repository.user_exists(command.deleted_by):
            raise AuditUserNotFound("deleted_by")

        now = self.clock.now()
        product.soft_delete(
            command.deleted_by,
            now,
            self.clock.format_log_timestamp(now),
        )
        return DeletedProductDTO.from_entity(self.repository.soft_delete(product))
