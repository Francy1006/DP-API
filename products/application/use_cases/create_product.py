from products.application.commands import CreateProductCommand
from products.application.dto import ProductDTO
from products.domain.entities import Product
from products.domain.exceptions import AuditUserNotFound, AuditUserRequired
from products.domain.repositories import Clock, ProductRepository


class CreateProduct:
    def __init__(self, repository: ProductRepository, clock: Clock):
        self.repository = repository
        self.clock = clock

    def execute(self, command: CreateProductCommand) -> ProductDTO:
        if not command.created_by:
            raise AuditUserRequired("created_by")
        if not self.repository.user_exists(command.created_by):
            raise AuditUserNotFound("created_by")

        product = Product(**command.__dict__)
        product.is_confirmed = bool(command.is_confirmed)
        now = self.clock.now()
        product.initialize_audit(now, self.clock.format_log_timestamp(now))
        return ProductDTO.from_entity(self.repository.create(product))
