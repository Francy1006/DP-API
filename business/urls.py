from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'item-filter-classifications', views.ItemFilterClassificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



