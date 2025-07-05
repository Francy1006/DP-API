from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-types', views.UserTypeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'user-tokens', views.UserTokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 