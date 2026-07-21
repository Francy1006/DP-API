class MaterialError(Exception):
    """Base exception for Material application and domain failures."""


class MaterialNotFound(MaterialError):
    pass


class MaterialAuditUserRequired(MaterialError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} is required")


class MaterialAuditUserNotFound(MaterialError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} does not identify an existing user")


class ImmutableMaterialField(MaterialError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} cannot be changed after Material creation")


class LegacyMaterialPriceInputRequired(MaterialError):
    """A legacy Material has no resolvable Price from which to infer inputs."""

    def __init__(self, missing_fields):
        self.missing_fields = tuple(missing_fields)
        super().__init__("Material price repair requires complete pricing inputs")
