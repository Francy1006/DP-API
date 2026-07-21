from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal

from django.test import SimpleTestCase
from django.urls import reverse

from pricing.domain.entities import Price, ProductPriceConfiguration
from pricing.domain.exceptions import CurrentPriceNotFound
from products.application.material_commands import (
    CreateMaterialCommand,
    DeleteMaterialCommand,
    UpdateMaterialCommand,
)
from products.application.use_cases.material import (
    CreateMaterial,
    DeleteMaterial,
    UpdateMaterial,
)
from products.domain.material_entities import Material
from products.domain.material_exceptions import (
    ImmutableMaterialField,
    LegacyMaterialPriceInputRequired,
)
from products.presentation.material_serializers import (
    MaterialCommandSerializer,
    MaterialSerializer,
)
from products.presentation.material_views import MaterialViewSet


ACTOR = "5fbf2886-4ad0-11f0-8ce6-0242ac120002"
MATERIAL_CODE = "21548b81-ec3e-4727-8496-b7e7f3185c34"
OLD_PRICE_CODE = "de1875d2-d9c6-4ecc-84cc-aa5811bbba15"
NEW_PRICE_CODE = "11111111-2222-3333-4444-555555555555"
CONFIGURATION = "e89311ca-d61e-4ead-b6cd-787c8b98f335"
NOW = datetime(2026, 7, 19, 16, 0, tzinfo=timezone.utc)
FORMULA = (
    "net_amount=${net_amount};"
    "iva_amount=${net_amount}*${iva};"
    "gross_amount=${net_amount}*(1+${iva});"
)


class FixedClock:
    def now(self):
        return NOW

    def format_log_timestamp(self, value):
        return "2026-07-19 16:00:00.000"


def material_entity(with_price=True):
    return Material(
        id=1,
        code=MATERIAL_CODE,
        sku="M-003-0001",
        description="MATERIAL DE PRUEBA",
        obs="OBSERVACIÓN",
        package_unit=1,
        min_package_purchase=1,
        price=OLD_PRICE_CODE,
        base_net_amount=Decimal("1000.00") if with_price else None,
        net_amount=Decimal("1000.00") if with_price else None,
        gross_amount=Decimal("1190.00") if with_price else None,
        iva_amount=Decimal("190.00") if with_price else None,
        aditional_tax_amount=Decimal("0.00") if with_price else None,
        retention_amount=Decimal("0.00") if with_price else None,
        price_configuration=CONFIGURATION if with_price else None,
        price_configuration_label=(
            "MATERIAL_NORMAL_IVA" if with_price else None
        ),
        provider=3,
        provider_name="COINPAL",
        type=3,
        type_name="MATERIAL",
        item_group=1,
        item_group_name="GRANEL",
        category=4,
        category_name="DESECHABLE",
        package=4,
        package_description="CAJA",
        created_by=ACTOR,
        log="init;",
    )


def current_price():
    return Price(
        code=OLD_PRICE_CODE,
        base_net_amount=Decimal("1000.00"),
        net_amount=Decimal("1000.00"),
        gross_amount=Decimal("1190.00"),
        iva_amount=Decimal("190.00"),
        aditional_tax_amount=Decimal("0.00"),
        retention_amount=Decimal("0.00"),
        price_configuration=CONFIGURATION,
        is_current=True,
        is_deleted=None,
        is_confirmed=None,
        created_at=NOW,
        created_by=ACTOR,
        record_item_code=MATERIAL_CODE,
        price_record_type=2,
    )


class FakeMaterialRepository:
    def __init__(self, material=None):
        self.material = material
        self.updated_fields = None
        self.submitted_sku = None

    def user_exists(self, code):
        return code == ACTOR

    def get(self, material_id):
        return self.material

    def get_for_update(self, material_id):
        return self.material

    def list(self, filters, search, ordering, active_only=False):
        return [self.material] if self.material else []

    def create(self, material):
        self.submitted_sku = material.sku
        material.id = 4
        material.sku = "M-003-0003"
        material.price_configuration_label = "MATERIAL_NORMAL_IVA"
        self.material = material
        return material

    def update(self, material, changed_fields):
        self.material = material
        self.updated_fields = changed_fields
        material.price_configuration_label = (
            "MATERIAL_NORMAL_IVA" if material.price_configuration else None
        )
        return material

    def soft_delete(self, material):
        self.material = material
        return material


class FakeMaterialPriceRepository:
    def __init__(self, price=None, missing=False, references=1):
        self.current = price or current_price()
        self.missing = missing
        self.references = references
        self.created = []
        self.deactivated = []

    def get_for_update(self, code):
        if self.missing:
            raise CurrentPriceNotFound
        return self.current

    def count_material_references(self, code):
        return self.references

    def get_material_configuration(self, code):
        return ProductPriceConfiguration(
            code=code,
            name="MATERIAL_NORMAL_IVA",
            record_type=2,
            variable_formula_code="material-formula-code",
            variable_formula_name="MATERIAL_STANDARD",
            formula_template=FORMULA,
        )

    def get_formula_variables(self, code):
        return {"iva": Decimal("0.190")}

    def create_version(
        self,
        components,
        configuration_code,
        product_code,
        created_at,
        created_by,
    ):
        price = Price(
            code=NEW_PRICE_CODE,
            base_net_amount=components.base_net_amount,
            net_amount=components.net_amount,
            gross_amount=components.gross_amount,
            iva_amount=components.iva_amount,
            aditional_tax_amount=components.aditional_tax_amount,
            retention_amount=components.retention_amount,
            price_configuration=configuration_code,
            is_current=True,
            is_deleted=None,
            is_confirmed=None,
            created_at=created_at,
            created_by=created_by,
            record_item_code=product_code,
            price_record_type=2,
        )
        self.created.append(price)
        return price

    def deactivate(self, code):
        self.deactivated.append(code)


class SnapshotTransactionManager:
    def __init__(self, materials, prices):
        self.materials = materials
        self.prices = prices

    @contextmanager
    def atomic(self):
        material_snapshot = deepcopy(self.materials.__dict__)
        price_snapshot = deepcopy(self.prices.__dict__)
        try:
            yield
        except Exception:
            self.materials.__dict__.clear()
            self.materials.__dict__.update(material_snapshot)
            self.prices.__dict__.clear()
            self.prices.__dict__.update(price_snapshot)
            raise


def update_use_case(materials, prices):
    return UpdateMaterial(
        materials,
        prices,
        SnapshotTransactionManager(materials, prices),
        FixedClock(),
    )


class MaterialContractTests(SimpleTestCase):
    def test_response_contract_and_legacy_null_price_components(self):
        data = MaterialSerializer(material_entity(with_price=False)).data

        self.assertEqual(data["price"], OLD_PRICE_CODE)
        self.assertIsNone(data["base_net_amount"])
        self.assertIsNone(data["price_configuration"])
        self.assertEqual(data["item_group"], 1)
        self.assertEqual(data["item_group_name"], "GRANEL")
        self.assertNotIn("log", data)

    def test_routes_and_methods_match_product(self):
        self.assertEqual(reverse("material-list"), "/api/materials/")
        self.assertEqual(reverse("material-detail", args=[1]), "/api/materials/1/")
        self.assertEqual(
            reverse("material-delete", args=[1]),
            "/api/materials/1/delete/",
        )
        self.assertEqual(
            MaterialViewSet.http_method_names,
            ["get", "post", "patch", "head", "options"],
        )

    def test_command_uses_item_group_and_protects_price_internals(self):
        fields = MaterialCommandSerializer().fields
        self.assertIn("item_group", fields)
        self.assertNotIn("group", fields)
        self.assertTrue(fields["price"].read_only)
        self.assertTrue(fields["sku"].read_only)

        serializer = MaterialCommandSerializer(
            data={"gross_amount": "1190"},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("gross_amount", serializer.errors)


class MaterialUseCaseTests(SimpleTestCase):
    def test_create_generates_price_and_leaves_sku_to_database(self):
        materials = FakeMaterialRepository()
        prices = FakeMaterialPriceRepository()
        command = CreateMaterialCommand(
            code=MATERIAL_CODE,
            description="NUEVO MATERIAL",
            obs="OBS",
            package_unit=1,
            min_package_purchase=1,
            base_net_amount=Decimal("1000"),
            price_configuration=CONFIGURATION,
            provider=3,
            type=3,
            item_group=1,
            category=4,
            package=4,
            created_by=ACTOR,
        )

        result = CreateMaterial(
            materials,
            prices,
            SnapshotTransactionManager(materials, prices),
            FixedClock(),
        ).execute(command)

        self.assertIsNone(materials.submitted_sku)
        self.assertEqual(result.sku, "M-003-0003")
        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(result.gross_amount, Decimal("1190.00"))
        self.assertEqual(prices.created[0].price_record_type, 2)
        self.assertEqual(prices.created[0].record_item_code, MATERIAL_CODE)
        self.assertEqual(result.version, 1)

    def test_regular_patch_audits_and_increments_version(self):
        materials = FakeMaterialRepository(material_entity())
        prices = FakeMaterialPriceRepository()

        result = update_use_case(materials, prices).execute(
            UpdateMaterialCommand(
                material_id=1,
                changes={"obs": "CAMBIO"},
                updated_by=ACTOR,
            )
        )

        self.assertEqual(result.version, 2)
        self.assertIn("PATCH: obs='CAMBIO'", materials.material.log)
        self.assertIn("version", materials.updated_fields)

    def test_provider_is_immutable(self):
        materials = FakeMaterialRepository(material_entity())
        with self.assertRaises(ImmutableMaterialField):
            update_use_case(materials, FakeMaterialPriceRepository()).execute(
                UpdateMaterialCommand(1, {"provider": 4}, ACTOR)
            )

    def test_price_patch_versions_owned_material_price(self):
        materials = FakeMaterialRepository(material_entity())
        prices = FakeMaterialPriceRepository()

        result = update_use_case(materials, prices).execute(
            UpdateMaterialCommand(
                1,
                {"base_net_amount": Decimal("2000")},
                ACTOR,
            )
        )

        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(result.gross_amount, Decimal("2380.00"))
        self.assertEqual(result.version, 2)
        self.assertEqual(prices.deactivated, [OLD_PRICE_CODE])

    def test_shared_price_is_forked_without_deactivation(self):
        materials = FakeMaterialRepository(material_entity())
        prices = FakeMaterialPriceRepository(references=3)

        result = update_use_case(materials, prices).execute(
            UpdateMaterialCommand(1, {"base_net_amount": Decimal("2000")}, ACTOR)
        )

        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(prices.deactivated, [])

    def test_legacy_material_requires_complete_inputs_then_repairs_link(self):
        materials = FakeMaterialRepository(material_entity(with_price=False))
        prices = FakeMaterialPriceRepository(missing=True)

        with self.assertRaises(LegacyMaterialPriceInputRequired) as raised:
            update_use_case(materials, prices).execute(
                UpdateMaterialCommand(
                    1,
                    {"base_net_amount": Decimal("1000")},
                    ACTOR,
                )
            )
        self.assertEqual(raised.exception.missing_fields, ("price_configuration",))

        result = update_use_case(materials, prices).execute(
            UpdateMaterialCommand(
                1,
                {
                    "base_net_amount": Decimal("1000"),
                    "price_configuration": CONFIGURATION,
                },
                ACTOR,
            )
        )
        self.assertEqual(result.price, NEW_PRICE_CODE)
        self.assertEqual(result.version, 2)
        self.assertEqual(prices.deactivated, [])

    def test_same_price_is_idempotent(self):
        materials = FakeMaterialRepository(material_entity())
        prices = FakeMaterialPriceRepository()

        result = update_use_case(materials, prices).execute(
            UpdateMaterialCommand(
                1,
                {"base_net_amount": Decimal("1000.00")},
                ACTOR,
            )
        )

        self.assertEqual(result.version, 1)
        self.assertEqual(prices.created, [])
        self.assertEqual(prices.deactivated, [])

    def test_soft_delete_preserves_row_contract(self):
        materials = FakeMaterialRepository(material_entity())
        result = DeleteMaterial(materials, FixedClock()).execute(
            DeleteMaterialCommand(1, ACTOR)
        )

        self.assertFalse(result.is_active)
        self.assertTrue(result.is_deleted)
        self.assertIn("DELETE: 2026-07-19", materials.material.log)
