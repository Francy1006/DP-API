from products.application.material_dto import MaterialDTO
from products.domain.material_repositories import MaterialRepository


class GetMaterial:
    def __init__(self, repository: MaterialRepository):
        self.repository = repository

    def execute(self, material_id: int) -> MaterialDTO:
        return MaterialDTO.from_entity(self.repository.get(material_id))
