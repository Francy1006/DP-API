from dataclasses import dataclass
from decimal import Decimal

from products.domain.repositories import PriceRepository
from pricing.domain.entities import PriceComponents, PriceConfiguration
from pricing.domain.policies import VariableFormulaPriceEngine


@dataclass(frozen=True)
class CalculatedProductPrice:
    configuration: PriceConfiguration
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
