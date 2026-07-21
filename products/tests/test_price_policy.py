from decimal import Decimal

from django.test import SimpleTestCase

from pricing.domain.exceptions import (
    FormulaResultUnavailable,
    FormulaVariableUnavailable,
    InvalidBaseNetAmount,
    InvalidVariableFormula,
)
from pricing.domain.policies import VariableFormulaPriceEngine


STANDARD_FORMULA = (
    "net_amount=${net_amount};"
    "iva_amount=${net_amount}*${iva};"
    "gross_amount=${net_amount}*(1+${iva});"
)


class VariableFormulaPriceEngineTests(SimpleTestCase):
    def setUp(self):
        self.engine = VariableFormulaPriceEngine()

    def test_evaluates_the_configured_product_formula_with_decimal(self):
        result = self.engine.calculate(
            base_net_amount=Decimal("16980"),
            formula_template=STANDARD_FORMULA,
            variables={"iva": Decimal("0.190")},
        )

        self.assertEqual(result.base_net_amount, Decimal("16980.00"))
        self.assertEqual(result.net_amount, Decimal("16980.00"))
        self.assertEqual(result.iva_amount, Decimal("3226.20"))
        self.assertEqual(result.gross_amount, Decimal("20206.20"))
        self.assertEqual(result.aditional_tax_amount, Decimal("0.00"))
        self.assertEqual(result.retention_amount, Decimal("0.00"))

    def test_does_not_round_intermediate_decimal_results(self):
        result = self.engine.calculate(
            base_net_amount=Decimal("1.49"),
            formula_template=STANDARD_FORMULA,
            variables={"iva": Decimal("0.190")},
        )

        self.assertEqual(result.base_net_amount, Decimal("1.49"))
        self.assertEqual(result.net_amount, Decimal("1.49"))
        self.assertEqual(result.iva_amount, Decimal("0.28"))
        self.assertEqual(result.gross_amount, Decimal("1.77"))

    def test_uses_round_half_up_only_for_final_storage_values(self):
        result = self.engine.calculate(
            base_net_amount=Decimal("0.50"),
            formula_template=(
                "net_amount=${net_amount};"
                "iva_amount=${net_amount}*0.01;"
                "gross_amount=${net_amount}+${iva_amount};"
            ),
            variables={},
        )

        self.assertEqual(result.base_net_amount, Decimal("0.50"))
        self.assertEqual(result.net_amount, Decimal("0.50"))
        self.assertEqual(result.iva_amount, Decimal("0.01"))
        self.assertEqual(result.gross_amount, Decimal("0.51"))

    def test_assignments_can_use_previous_formula_results(self):
        result = self.engine.calculate(
            base_net_amount=Decimal("100.25"),
            formula_template=(
                "net_amount=${net_amount};"
                "iva_amount=${net_amount}*${iva};"
                "gross_amount=${net_amount}+${iva_amount};"
            ),
            variables={"iva": Decimal("0.19")},
        )

        self.assertEqual(result.net_amount, Decimal("100.25"))
        self.assertEqual(result.iva_amount, Decimal("19.05"))
        self.assertEqual(result.gross_amount, Decimal("119.30"))

    def test_rejects_missing_variables_or_required_results(self):
        with self.assertRaises(FormulaVariableUnavailable):
            self.engine.calculate(
                Decimal("100"),
                STANDARD_FORMULA,
                variables={},
            )
        with self.assertRaises(FormulaResultUnavailable):
            self.engine.calculate(
                Decimal("100"),
                "net_amount=${net_amount};",
                variables={},
            )

    def test_rejects_unsafe_python_instead_of_using_eval(self):
        unsafe_formulas = (
            "net_amount=__import__('os');iva_amount=0;gross_amount=0;",
            "net_amount=(1).__class__;iva_amount=0;gross_amount=0;",
            "net_amount=2**8;iva_amount=0;gross_amount=0;",
        )
        for formula in unsafe_formulas:
            with self.subTest(formula=formula):
                with self.assertRaises(InvalidVariableFormula):
                    self.engine.calculate(
                        Decimal("100"),
                        formula,
                        variables={},
                    )

    def test_rejects_non_positive_or_invalid_base_amount(self):
        for invalid in (0, -1, True, "invalid"):
            with self.subTest(value=invalid):
                with self.assertRaises(InvalidBaseNetAmount):
                    self.engine.calculate(
                        invalid,
                        STANDARD_FORMULA,
                        variables={"iva": Decimal("0.19")},
                    )

    def test_rejects_results_that_exceed_the_current_integer_columns(self):
        with self.assertRaises(FormulaResultUnavailable):
            self.engine.calculate(
                Decimal("999999999999.99"),
                STANDARD_FORMULA,
                variables={"iva": Decimal("0.19")},
            )
