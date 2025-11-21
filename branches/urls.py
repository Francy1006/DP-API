from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'branch-types', views.BranchTypeViewSet)
router.register(r'branches', views.BranchViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'platform-details', views.PlatformDetailViewSet)
router.register(r'company-agreements', views.CompanyAgreementViewSet)
router.register(r'agreements', views.AgreementViewSet)
router.register(r'agreement-details', views.AgreementDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]







