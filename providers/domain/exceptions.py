class ProviderError(Exception):
    """Base exception for Provider domain and application failures."""


class ProviderNotFound(ProviderError):
    pass
