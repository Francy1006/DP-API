from products.application.commands import ListProductsQuery
from products.application.dto import ProductDTO
from products.domain.repositories import ProductRepository


class ListProducts:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, query: ListProductsQuery) -> list[ProductDTO]:
        products = self.repository.list(
            filters=query.filters,
            search=query.search,
            ordering=query.ordering,
            active_only=query.active_only,
        )
        return [ProductDTO.from_entity(product) for product in products]
