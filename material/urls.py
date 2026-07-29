from django.urls import include, path
from rest_framework.routers import DefaultRouter

from material.presentation.views import MaterialViewSet


router = DefaultRouter()
router.register(r"materials", MaterialViewSet, basename="material")

urlpatterns = [
    path("", include(router.urls)),
]
