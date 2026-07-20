import ast
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .entities import PriceComponents
from .exceptions import (
    FormulaResultUnavailable,
    FormulaVariableUnavailable,
    InvalidBaseNetAmount,
    InvalidVariableFormula,
)


VARIABLE_REFERENCE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
ASSIGNMENT_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class _DecimalExpressionEvaluator:
    binary_operators = {
        ast.Add: lambda left, right: left + right,
        ast.Sub: lambda left, right: left - right,
        ast.Mult: lambda left, right: left * right,
        ast.Div: lambda left, right: left / right,
    }
    unary_operators = {
        ast.UAdd: lambda value: value,
        ast.USub: lambda value: -value,
    }

    def evaluate(self, expression, variables):
        try:
            parsed = ast.parse(expression, mode="eval")
            return self._visit(parsed.body, variables)
        except FormulaVariableUnavailable:
            raise
        except (InvalidOperation, ZeroDivisionError, SyntaxError) as error:
            raise InvalidVariableFormula from error

    def _visit(self, node, variables):
        if isinstance(node, ast.BinOp) and type(node.op) in self.binary_operators:
            return self.binary_operators[type(node.op)](
                self._visit(node.left, variables),
                self._visit(node.right, variables),
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.unary_operators:
            return self.unary_operators[type(node.op)](
                self._visit(node.operand, variables)
            )
        if isinstance(node, ast.Name):
            try:
                return variables[node.id]
            except KeyError as error:
                raise FormulaVariableUnavailable(node.id) from error
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool):
            if isinstance(node.value, (int, float)):
                return Decimal(str(node.value))
        raise InvalidVariableFormula(
            f"Unsupported expression element: {type(node).__name__}"
        )


class VariableFormulaPriceEngine:
    """Safe sequential evaluator for configured Price arithmetic."""

    storage_unit = Decimal("0.01")
    storage_min = Decimal("-999999999999.99")
    storage_max = Decimal("999999999999.99")
    output_fields = {
        "net_amount",
        "gross_amount",
        "iva_amount",
        "aditional_tax_amount",
        "retention_amount",
    }

    def __init__(self):
        self.expression_evaluator = _DecimalExpressionEvaluator()

    def calculate(self, base_net_amount, formula_template, variables):
        try:
            base_net = Decimal(str(base_net_amount))
        except (InvalidOperation, ValueError) as error:
            raise InvalidBaseNetAmount from error
        if not base_net.is_finite() or base_net <= 0:
            raise InvalidBaseNetAmount

        context = {
            key: Decimal(str(value))
            for key, value in variables.items()
        }
        # Price formulas use net_amount as the editable base value. Keep the
        # original decimal throughout the engine and round only for storage.
        context["base_net_amount"] = base_net
        context["net_amount"] = base_net
        results = {}

        assignments = [
            value.strip()
            for value in formula_template.split(";")
            if value.strip()
        ]
        if not assignments:
            raise InvalidVariableFormula("The formula has no assignments")

        for assignment in assignments:
            if "=" not in assignment:
                raise InvalidVariableFormula("Invalid formula assignment")
            field_name, expression = assignment.split("=", 1)
            field_name = field_name.strip()
            if not ASSIGNMENT_NAME.fullmatch(field_name):
                raise InvalidVariableFormula("Invalid result field")
            normalized_expression = VARIABLE_REFERENCE.sub(
                lambda match: match.group(1),
                expression.strip(),
            )
            value = self.expression_evaluator.evaluate(
                normalized_expression,
                {**context, **results},
            )
            if not value.is_finite():
                raise InvalidVariableFormula("Formula returned a non-finite value")
            results[field_name] = value

        missing = {"net_amount", "gross_amount", "iva_amount"} - results.keys()
        if missing:
            raise FormulaResultUnavailable(", ".join(sorted(missing)))

        rounded = {
            field_name: self._round_for_storage(
                results.get(field_name, Decimal("0"))
            )
            for field_name in self.output_fields
        }
        return PriceComponents(
            base_net_amount=self._round_for_storage(base_net),
            net_amount=rounded["net_amount"],
            gross_amount=rounded["gross_amount"],
            iva_amount=rounded["iva_amount"],
            aditional_tax_amount=rounded["aditional_tax_amount"],
            retention_amount=rounded["retention_amount"],
        )

    def _round_for_storage(self, value):
        rounded = value.quantize(
            self.storage_unit,
            rounding=ROUND_HALF_UP,
        )
        if not self.storage_min <= rounded <= self.storage_max:
            raise FormulaResultUnavailable("Result exceeds DECIMAL(14,2) storage")
        return rounded
