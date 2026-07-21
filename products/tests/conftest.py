import pytest
from rest_framework.test import APIClient

from products.tests.factories import build_product


@pytest.fixture
def product_factory():
    """Return the deterministic Product domain builder."""

    return build_product


@pytest.fixture
def api_client():
    """Return an authenticated DRF client without creating database users."""

    client = APIClient()
    user = type("AuthenticatedTestUser", (), {"is_authenticated": True})()
    client.force_authenticate(user=user)
    return client
