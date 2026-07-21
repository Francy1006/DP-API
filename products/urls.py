from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menus', views.MenuViewSet)
router.register(r'item-categories', views.ItemCategoryViewSet)
router.register(r'item-types', views.ItemTypeViewSet)
router.register(r'item-groups', views.ItemGroupViewSet)
router.register(r'package-types', views.PackageTypeViewSet)
router.register(r'transport-types', views.TransportTypeViewSet)
router.register(r'measure-units', views.MeasureUnitViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'item-configurations', views.ItemConfigurationViewSet)
router.register(r'item-configuration-details', views.ItemConfigurationDetailViewSet)
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'services', views.ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
