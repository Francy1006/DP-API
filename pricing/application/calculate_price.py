from dataclasses import dataclass
from decimal import Decimal

from pricing.domain.entities import PriceComponents, ProductPriceConfiguration
from pricing.domain.policies import VariableFormulaPriceEngine
from pricing.domain.repositories import PriceRepository


@dataclass(frozen=True)
class CalculatedProductPrice:
    configuration: ProductPriceConfiguration
    components: PriceComponents


class CalculateProductPrice:
    def __init__(self, repository: PriceRepository):
        self.repository = repository
        self.engine = VariableFormulaPriceEngine()

    def execute(
        self,
        base_net_amount: Decimal,
        configuration_code: str,
    ) -> CalculatedProductPrice:
        configuration = self.repository.get_product_configuration(
            configuration_code
        )
        variables = self.repository.get_formula_variables(configuration.code)
        components = self.engine.calculate(
            base_net_amount=base_net_amount,
            formula_template=configuration.formula_template,
            variables=variables,
        )
        return CalculatedProductPrice(
            configuration=configuration,
            components=components,
        )
