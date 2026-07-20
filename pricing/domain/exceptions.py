class PricingError(Exception):
    """Base exception for safe Price versioning failures."""


class InvalidBaseNetAmount(PricingError):
    pass


class CurrentPriceNotFound(PricingError):
    pass


class UnsafeCurrentPrice(PricingError):
    pass


class ProductPriceConfigurationUnavailable(PricingError):
    pass


class FiscalDirectiveUnavailable(PricingError):
    pass


class InvalidVariableFormula(PricingError):
    pass


class FormulaVariableUnavailable(PricingError):
    pass


class FormulaResultUnavailable(PricingError):
    pass
