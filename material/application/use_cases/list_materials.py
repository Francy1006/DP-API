from material.application.commands import ListMaterialsQuery
from material.application.dto import MaterialDTO
from material.domain.repositories import MaterialRepository


class ListMaterials:
    def __init__(self, repository: MaterialRepository):
        self.repository = repository

    def execute(self, query: ListMaterialsQuery) -> list[MaterialDTO]:
        materials = self.repository.list(
            filters=query.filters,
            search=query.search,
            ordering=query.ordering,
            active_only=query.active_only,
        )
        return [MaterialDTO.from_entity(material) for material in materials]
