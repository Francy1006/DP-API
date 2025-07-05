from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'fiscal-directive-types', views.FiscalDirectiveTypeViewSet)
router.register(r'fiscal-directives', views.FiscalDirectiveViewSet)
router.register(r'fiscal-formulas', views.FiscalFormulaViewSet)
router.register(r'price-fiscal-configurations', views.PriceFiscalConfigurationViewSet)
router.register(r'prices', views.PriceViewSet)
router.register(r'fiscal-configuration-details', views.FiscalConfigurationDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 