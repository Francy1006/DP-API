from products.application.dto import ProductDTO
from products.domain.repositories import ProductRepository


class GetProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int) -> ProductDTO:
        return ProductDTO.from_entity(self.repository.get(product_id))
