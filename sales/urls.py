from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Rutas placeholder para futuras implementaciones de ventas

urlpatterns = [
    path('', include(router.urls)),
] 