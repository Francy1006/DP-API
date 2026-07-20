from decimal import Decimal
from uuid import uuid4

from django.db import connection

from pricing.domain.entities import (
    Price,
    ProductPriceConfiguration,
)
from pricing.domain.exceptions import (
    CurrentPriceNotFound,
    FiscalDirectiveUnavailable,
    ProductPriceConfigurationUnavailable,
    UnsafeCurrentPrice,
)
from pricing.models import Price as PriceModel
from products.models import Product as ProductModel


class DjangoPriceRepository:
    """ORM/SQL adapter limited to the Product price-versioning slice."""

    @staticmethod
    def _to_entity(model):
        return Price(
            code=model.code,
            base_net_amount=model.base_net_amount,
            net_amount=model.net_amount,
            gross_amount=model.gross_amount,
            iva_amount=model.iva_amount,
            aditional_tax_amount=model.aditional_tax_amount,
            retention_amount=model.retention_amount,
            price_configuration=model.price_configuration,
            is_current=model.is_current,
            is_deleted=model.is_deleted,
            is_confirmed=model.is_confirmed,
            created_at=model.created_at,
            created_by=model.created_by_id,
            record_item_code=model.record_item_code,
            price_record_type=model.price_record_type,
        )

    def get_for_update(self, price_code):
        try:
            model = PriceModel.objects.select_for_update().get(code=price_code)
        except PriceModel.DoesNotExist as error:
            raise CurrentPriceNotFound from error
        return self._to_entity(model)

    def count_product_references(self, price_code):
        # Include soft-deleted Products: their foreign-key reference still exists.
        return ProductModel.objects.filter(price_id=price_code).count()

    def get_product_configuration(self, configuration_code):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT pc.code,
                       pc.price_configuration,
                       pc.record_type,
                       vf.code,
                       vf.formula,
                       vf.formula_template
                FROM ditaly_pasta.price_configuration AS pc
                INNER JOIN sbm_business.variable_formula AS vf
                    ON vf.code = pc.variable_formula
                INNER JOIN sbm_business.formula_type AS ft
                    ON ft.id = vf.formula_type
                WHERE pc.code = %s
                  AND pc.record_type = 1
                  AND pc.is_confirmed IS TRUE
                  AND pc.is_deleted IS NOT TRUE
                  AND vf.is_confirmed IS TRUE
                  AND vf.is_deleted IS NOT TRUE
                  AND ft.type = 'PRICE'
                """,
                [configuration_code],
            )
            rows = cursor.fetchall()
        if len(rows) != 1:
            raise ProductPriceConfigurationUnavailable
        (
            code,
            name,
            record_type,
            variable_formula_code,
            variable_formula_name,
            formula_template,
        ) = rows[0]
        return ProductPriceConfiguration(
            code=code,
            name=name,
            record_type=record_type,
            variable_formula_code=variable_formula_code,
            variable_formula_name=variable_formula_name,
            formula_template=formula_template,
        )

    def get_formula_variables(self, configuration_code):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT fcd.var, fd.value
                FROM ditaly_pasta.fiscal_configuration_detail AS fcd
                INNER JOIN sbm_business.fiscal_directive AS fd
                    ON fd.code = fcd.fiscal_directive
                WHERE fcd.module_config_id = %s
                  AND fcd.is_active IS TRUE
                  AND fd.is_confirmed IS TRUE
                  AND fd.is_deleted IS NOT TRUE
                """,
                [configuration_code],
            )
            rows = cursor.fetchall()
        variables = {}
        for variable, value in rows:
            if not variable or value is None or variable in variables:
                raise FiscalDirectiveUnavailable
            variables[variable] = Decimal(value)
        return variables

    def create_version(
        self,
        components,
        configuration_code,
        product_code,
        created_at,
        created_by,
    ):
        model = PriceModel.objects.create(
            code=str(uuid4()),
            base_net_amount=components.base_net_amount,
            net_amount=components.net_amount,
            gross_amount=components.gross_amount,
            iva_amount=components.iva_amount,
            aditional_tax_amount=components.aditional_tax_amount,
            retention_amount=components.retention_amount,
            price_configuration=configuration_code,
            is_current=True,
            created_at=created_at,
            created_by_id=created_by,
            record_item_code=product_code,
            price_record_type=1,
        )
        return self._to_entity(model)

    def deactivate(self, price_code):
        updated = PriceModel.objects.filter(
            code=price_code,
            is_current=True,
        ).update(is_current=False)
        if updated != 1:
            raise UnsafeCurrentPrice
