from django.test import SimpleTestCase
from django.urls import reverse

from providers.application.commands import ListProvidersQuery
from providers.application.use_cases import ListProviders
from providers.domain.entities import Provider
from providers.presentation.serializers import (
    ProviderCommandSerializer,
    ProviderSerializer,
)
from providers.presentation.views import ProviderViewSet


class FakeProviderRepository:
    def list(self, filters, search, ordering):
        return [
            Provider(
                id=1,
                code="PVP-001",
                provider="VERONA - PASIONES ITALIANAS",
                type=1,
                type_name="PRODUCTOR",
                rating=4,
                obs_provider="Proveedor de pastas y salsas",
                created_by="5fbf2886-4ad0-11f0-8ce6-0242ac120002",
            )
        ]


class ProviderContractTests(SimpleTestCase):
    def test_selector_fields_are_available(self):
        fields = ProviderSerializer().fields
        command_fields = ProviderCommandSerializer().fields

        self.assertIn("id", fields)
        self.assertIn("provider", fields)
        self.assertIn("type_name", fields)
        self.assertIn("dispatch_district_name", command_fields)
        self.assertIn("dispatch_region_name", command_fields)

    def test_routes_and_methods_remain_available(self):
        self.assertEqual(reverse("provider-list"), "/api/providers/")
        self.assertEqual(reverse("provider-detail", args=[1]), "/api/providers/1/")
        self.assertEqual(
            ProviderViewSet.http_method_names,
            [
                "get",
                "post",
                "put",
                "patch",
                "delete",
                "head",
                "options",
                "trace",
            ],
        )

    def test_list_use_case_returns_selector_data(self):
        result = ListProviders(FakeProviderRepository()).execute(
            ListProvidersQuery()
        )

        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].provider, "VERONA - PASIONES ITALIANAS")
