from dataclasses import dataclass
from decimal import Decimal

from pricing.domain.entities import PriceComponents, PriceConfiguration
from pricing.domain.policies import VariableFormulaPriceEngine
from material.domain.repositories import MaterialPriceRepository


@dataclass(frozen=True)
class CalculatedMaterialPrice:
    configuration: PriceConfiguration
    components: PriceComponents


class CalculateMaterialPrice:
    def __init__(self, repository: MaterialPriceRepository):
        self.repository = repository
        self.engine = VariableFormulaPriceEngine()

    def execute(
        self,
        base_net_amount: Decimal,
        configuration_code: str,
    ) -> CalculatedMaterialPrice:
        configuration = self.repository.get_material_configuration(
            configuration_code
        )
        variables = self.repository.get_formula_variables(configuration.code)
        components = self.engine.calculate(
            base_net_amount=base_net_amount,
            formula_template=configuration.formula_template,
            variables=variables,
        )
        return CalculatedMaterialPrice(
            configuration=configuration,
            components=components,
        )
