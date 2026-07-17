from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'provider-types', views.ProviderTypeViewSet)
router.register(r'provider-groups', views.ProviderGroupViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'banks', views.BankViewSet)
router.register(r'bank-account-types', views.BankAccountTypeViewSet)
router.register(r'providers', views.ProviderViewSet, basename='provider')

urlpatterns = [
    path('', include(router.urls)),
]
