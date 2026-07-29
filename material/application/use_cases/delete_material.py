from material.application.commands import DeleteMaterialCommand
from material.application.dto import DeletedMaterialDTO
from material.domain.exceptions import (
    MaterialAuditUserNotFound,
    MaterialAuditUserRequired,
)
from material.domain.repositories import MaterialClock, MaterialRepository


class DeleteMaterial:
    def __init__(self, repository: MaterialRepository, clock: MaterialClock):
        self.repository = repository
        self.clock = clock

    def execute(self, command: DeleteMaterialCommand) -> DeletedMaterialDTO:
        material = self.repository.get(command.material_id)
        if not command.deleted_by:
            raise MaterialAuditUserRequired("deleted_by")
        if not self.repository.user_exists(command.deleted_by):
            raise MaterialAuditUserNotFound("deleted_by")

        now = self.clock.now()
        material.soft_delete(
            command.deleted_by,
            now,
            self.clock.format_log_timestamp(now),
        )
        return DeletedMaterialDTO.from_entity(
            self.repository.soft_delete(material)
        )
