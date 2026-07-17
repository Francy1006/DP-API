class ProductError(Exception):
    """Base exception for Product application and domain failures."""


class ProductNotFound(ProductError):
    pass


class AuditUserRequired(ProductError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} is required")


class AuditUserNotFound(ProductError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} does not identify an existing user")


class ImmutableProductField(ProductError):
    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"{field_name} cannot be changed after Product creation")
