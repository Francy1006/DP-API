from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'instruction-types', views.InstructionTypeViewSet)
router.register(r'instructions', views.InstructionViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 