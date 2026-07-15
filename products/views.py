from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from users.models import User
from .models import (
    Menu,
    ItemCategory,
    ItemType,
    ItemGroup,
    PackageType,
    TransportType,
    MeasureUnit,
    Package,
    Catalog,
    ItemConfiguration,
    ItemConfigurationDetail,
    Product,
    Material,
    Service,
)
from .serializers import (
    MenuSerializer,
    ItemCategorySerializer,
    ItemTypeSerializer,
    ItemGroupSerializer,
    PackageTypeSerializer,
    TransportTypeSerializer,
    MeasureUnitSerializer,
    PackageSerializer,
    CatalogSerializer,
    ItemConfigurationSerializer,
    ItemConfigurationDetailSerializer,
    ProductSerializer,
    MaterialSerializer,
    ServiceSerializer,
)

# Create your views here.


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["menu"]
    search_fields = ["menu", "description"]
    ordering_fields = ["menu", "description"]
    ordering = ["menu"]


class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "catalog_render"]
    search_fields = ["category", "description"]
    ordering_fields = ["category", "description"]
    ordering = ["category"]

    @action(detail=False, methods=["get"])
    def catalog_categories(self, request):
        """Obtener solo categorías que se renderizan en catálogo"""
        catalog_categories = self.queryset.filter(catalog_render=True)
        serializer = self.get_serializer(catalog_categories, many=True)
        return Response(serializer.data)


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type"]
    search_fields = ["type", "description"]
    ordering_fields = ["type", "description"]
    ordering = ["type"]


class ItemGroupViewSet(viewsets.ModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["group_name", "catalog_render"]
    search_fields = ["group_name", "description"]
    ordering_fields = ["group_name", "description"]
    ordering = ["group_name"]

    @action(detail=False, methods=["get"])
    def catalog_groups(self, request):
        """Obtener solo grupos que se renderizan en catálogo"""
        catalog_groups = self.queryset.filter(catalog_render=True)
        serializer = self.get_serializer(catalog_groups, many=True)
        return Response(serializer.data)


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type"]
    search_fields = ["type", "description"]
    ordering_fields = ["type", "description"]
    ordering = ["type"]


class TransportTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportType.objects.all()
    serializer_class = TransportTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type"]
    search_fields = ["type", "description"]
    ordering_fields = ["type", "description"]
    ordering = ["type"]


class MeasureUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["measure_unit"]
    search_fields = ["measure_unit", "description"]
    ordering_fields = ["measure_unit", "description"]
    ordering = ["measure_unit"]


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["package_type", "transport_type", "is_deleted", "is_confirmed"]
    search_fields = ["description"]
    ordering_fields = ["description", "created_at"]
    ordering = ["description"]


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "menu",
        "group",
        "category",
        "type",
        "chef_recommendation",
        "is_visible",
        "is_deleted",
        "is_confirmed",
    ]
    search_fields = ["name", "sku", "description"]
    ordering_fields = ["name", "sku", "created_at"]
    ordering = ["-created_at"]

    @action(detail=False, methods=["get"])
    def visible(self, request):
        """Obtener solo catálogos visibles"""
        visible_catalogs = self.queryset.filter(is_visible=True)
        serializer = self.get_serializer(visible_catalogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def chef_recommendations(self, request):
        """Obtener solo catálogos recomendados por el chef"""
        chef_recommendations = self.queryset.filter(
            chef_recommendation=True,
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True,
        )
        serializer = self.get_serializer(chef_recommendations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def salsas(self, request):
        """Obtener solo catálogos de salsas"""
        salsas = self.queryset.filter(
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True,
            category_id=2,  # ID de la categoría "salsa"
        )
        serializer = self.get_serializer(salsas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pastas(self, request):
        """Obtener solo catálogos de pastas"""
        pastas = self.queryset.filter(
            is_visible=True,
            is_confirmed=True,
            is_deleted__isnull=True,
            category_id=1,  # ID de la categoría "pasta"
        )
        serializer = self.get_serializer(pastas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def franchise_only_catalogs(self, request):
        """Obtener catálogos confirmados, activos, no eliminados y solo de franquicia"""
        franchise_only_catalogs = self.queryset.filter(
            is_confirmed=True,
            is_visible=True,  # equivalente a is_active para catálogos
            is_deleted__isnull=True,
            menu__franchise_only=True,
        )
        serializer = self.get_serializer(franchise_only_catalogs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def toggle_visibility(self, request, pk=None):
        """Alternar visibilidad del catálogo"""
        catalog = self.get_object()
        catalog.is_visible = not catalog.is_visible
        catalog.save()
        serializer = self.get_serializer(catalog)
        return Response(serializer.data)


class ItemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = ItemConfiguration.objects.all()
    serializer_class = ItemConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["package", "is_deleted", "is_confirmed"]
    search_fields = ["code", "configuration", "description"]
    ordering_fields = ["configuration", "created_at"]
    ordering = ["configuration"]


class ItemConfigurationDetailViewSet(viewsets.ModelViewSet):
    queryset = ItemConfigurationDetail.objects.all()
    serializer_class = ItemConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "configuration", "is_deleted", "is_confirmed"]
    search_fields = ["code", "detail", "id_item"]
    ordering_fields = ["code", "detail"]
    ordering = ["code"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(Q(is_deleted=False) | Q(is_deleted__isnull=True))
    serializer_class = ProductSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "provider",
        "type",
        "item_group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
    ]
    search_fields = ["code", "sku", "description"]
    ordering_fields = ["description", "created_at"]
    ordering = ["description"]

    @staticmethod
    def _format_log_timestamp(value):
        return timezone.localtime(value).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def perform_create(self, serializer):
        created_by = serializer.validated_data.get("created_by")
        if created_by is None:
            raise ValidationError({"created_by": "Este campo es requerido."})

        created_at = timezone.now()
        created_at_log = self._format_log_timestamp(created_at)
        serializer.save(
            created_at=created_at,
            log=f"INIT: {created_at_log} (USER: {created_by.code});",
        )

    def perform_update(self, serializer):
        updated_by = serializer.validated_data.get("updated_by")
        if updated_by is None:
            raise ValidationError({"updated_by": "Este campo es requerido."})

        product = serializer.instance
        changes = []

        for field_name, new_value in serializer.validated_data.items():
            if field_name == "updated_by":
                continue

            model_field = product._meta.get_field(field_name)
            if model_field.is_relation:
                log_value = getattr(new_value, model_field.target_field.attname)
                current_value = getattr(product, model_field.attname)
            else:
                log_value = new_value
                current_value = getattr(product, field_name)

            if current_value != log_value:
                changes.append(f"{field_name}={log_value!r}")

        current_log = (product.log or "").strip()
        if current_log and not current_log.endswith(";"):
            current_log = f"{current_log};"

        changes_log = ", ".join(changes) if changes else "sin cambios"
        patch_log = f"PATCH: {changes_log} (USER: {updated_by.code});"
        updated_log = f"{current_log} {patch_log}".strip()

        serializer.save(
            updated_at=timezone.now(),
            log=updated_log,
        )

    @action(detail=True, methods=["post"], url_path="delete", url_name="delete")
    def soft_delete(self, request, pk=None):
        product = self.get_object()
        deleted_by_code = request.data.get("deleted_by")

        if not deleted_by_code:
            return Response(
                {"deleted_by": "Este campo es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            deleted_by = User.objects.get(code=deleted_by_code)
        except User.DoesNotExist:
            return Response(
                {"deleted_by": "El usuario indicado no existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_at = timezone.now()
        deleted_at_log = self._format_log_timestamp(deleted_at)
        current_log = (product.log or "").strip()
        if current_log and not current_log.endswith(";"):
            current_log = f"{current_log};"

        product.is_active = False
        product.is_deleted = True
        product.deleted_at = deleted_at
        product.deleted_by = deleted_by
        product.log = (
            f"{current_log} DELETE: {deleted_at_log} (USER: {deleted_by.code});"
        ).strip()
        product.save(
            update_fields=[
                "is_active",
                "is_deleted",
                "deleted_at",
                "deleted_by",
                "log",
            ]
        )

        return Response(
            {
                "id": product.id,
                "is_active": product.is_active,
                "is_deleted": product.is_deleted,
                "deleted_at": product.deleted_at,
                "deleted_by": product.deleted_by_id,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Obtener solo productos activos"""
        active_products = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_products, many=True)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "provider",
        "type",
        "group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
    ]
    search_fields = ["code", "sku", "description"]
    ordering_fields = ["description", "created_at"]
    ordering = ["description"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Obtener solo materiales activos"""
        active_materials = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_materials, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "provider",
        "type",
        "group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
    ]
    search_fields = ["code", "sku", "description"]
    ordering_fields = ["description", "created_at"]
    ordering = ["description"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Obtener solo servicios activos"""
        active_services = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_services, many=True)
        return Response(serializer.data)
