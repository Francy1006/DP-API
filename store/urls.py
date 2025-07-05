from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configurar el router para ViewSets
router = DefaultRouter()
router.register(r'menus', views.MenuViewSet)
router.register(r'item-categories', views.ItemCategoryViewSet)
router.register(r'item-types', views.ItemTypeViewSet)
router.register(r'item-groups', views.ItemGroupViewSet)
router.register(r'instruction-types', views.InstructionTypeViewSet)
router.register(r'instructions', views.InstructionViewSet)
router.register(r'package-types', views.PackageTypeViewSet)
router.register(r'transport-types', views.TransportTypeViewSet)
router.register(r'measure-units', views.MeasureUnitViewSet)
router.register(r'provider-types', views.ProviderTypeViewSet)
router.register(r'bank-account-types', views.BankAccountTypeViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'banks', views.BankViewSet)
router.register(r'user-types', views.UserTypeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'user-tokens', views.UserTokenViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'providers', views.ProviderViewSet)

# URLs para ViewSets
urlpatterns = [
    path('', include(router.urls)),
]
