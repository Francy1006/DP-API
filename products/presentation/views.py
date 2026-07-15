from types import SimpleNamespace

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from products.application.commands import (
    CreateProductCommand,
    DeleteProductCommand,
    ListProductsQuery,
    UpdateProductCommand,
)
from products.application.use_cases import (
    CreateProduct,
    DeleteProduct,
    GetProduct,
    ListProducts,
    UpdateProduct,
)
from products.domain.exceptions import (
    AuditUserNotFound,
    AuditUserRequired,
    ProductNotFound,
)
from products.infrastructure.clock import DjangoClock
from products.infrastructure.repositories import DjangoProductRepository
from products.presentation.serializers import (
    DeletedProductSerializer,
    ProductCommandSerializer,
    ProductFilterSerializer,
    ProductSerializer,
)


RELATION_VALUE_FIELDS = {
    "price": "code",
    "provider": "pk",
    "type": "pk",
    "item_group": "pk",
    "category": "pk",
    "package": "pk",
    "created_by": "code",
    "confirmed_by": "code",
    "updated_by": "code",
}


def _primitive_values(validated_data):
    values = {}
    for field_name, value in validated_data.items():
        attribute = RELATION_VALUE_FIELDS.get(field_name)
        values[field_name] = (
            getattr(value, attribute)
            if value is not None and attribute
            else value
        )
    return values


class ProductViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """REST adapter. Every Product operation delegates to an application use case."""

    serializer_class = ProductCommandSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    filter_fields = (
        "provider",
        "type",
        "item_group",
        "category",
        "is_active",
        "is_deleted",
        "is_confirmed",
    )
    ordering_fields = {"description", "created_at"}

    def get_repository(self):
        return DjangoProductRepository()

    def get_clock(self):
        return DjangoClock()

    @staticmethod
    def _raise_api_error(error):
        if isinstance(error, ProductNotFound):
            raise NotFound
        if isinstance(error, AuditUserRequired):
            raise ValidationError({error.field_name: "Este campo es requerido."})
        if isinstance(error, AuditUserNotFound):
            raise ValidationError(
                {error.field_name: "El usuario indicado no existe."}
            )
        raise error

    def _get_product(self, product_id):
        try:
            return GetProduct(self.get_repository()).execute(product_id)
        except (ProductNotFound, AuditUserRequired, AuditUserNotFound) as error:
            self._raise_api_error(error)

    def list(self, request, *args, **kwargs):
        filter_serializer = ProductFilterSerializer(
            data={
                name: request.query_params[name]
                for name in self.filter_fields
                if name in request.query_params
            }
        )
        filter_serializer.is_valid(raise_exception=True)

        ordering = []
        for field_name in request.query_params.get("ordering", "description").split(","):
            normalized = field_name.lstrip("-")
            if normalized in self.ordering_fields:
                ordering.append(field_name)
        if not ordering:
            ordering = ["description"]

        query = ListProductsQuery(
            filters=filter_serializer.validated_data,
            search=request.query_params.get("search") or None,
            ordering=tuple(ordering),
        )
        products = ListProducts(self.get_repository()).execute(query)
        page = self.paginate_queryset(products)
        if page is not None:
            data = ProductSerializer(page, many=True).data
            return self.get_paginated_response(data)
        return Response(ProductSerializer(products, many=True).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        product = self._get_product(pk)
        return Response(ProductSerializer(product).data)

    def create(self, request, *args, **kwargs):
        serializer = ProductCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = _primitive_values(serializer.validated_data)
        command = CreateProductCommand(
            code=values["code"],
            sku=values["sku"],
            description=values["description"],
            obs=values["obs"],
            package_unit=values["package_unit"],
            min_package_purchase=values["min_package_purchase"],
            price=values["price"],
            provider=values["provider"],
            type=values["type"],
            item_group=values["item_group"],
            category=values["category"],
            package=values["package"],
            created_by=values["created_by"],
            url=values.get("url"),
            is_active=values.get("is_active", True),
            is_confirmed=values.get("is_confirmed"),
            confirmed_by=values.get("confirmed_by"),
            updated_by=values.get("updated_by"),
        )
        try:
            product = CreateProduct(self.get_repository(), self.get_clock()).execute(
                command
            )
        except (ProductNotFound, AuditUserRequired, AuditUserNotFound) as error:
            self._raise_api_error(error)
        response_data = ProductSerializer(product).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(response_data),
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        current = self._get_product(pk)
        serializer = ProductCommandSerializer(
            instance=SimpleNamespace(pk=current.id),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        values = _primitive_values(serializer.validated_data)
        updated_by = values.pop("updated_by", None)
        command = UpdateProductCommand(
            product_id=current.id,
            changes=values,
            updated_by=updated_by,
        )
        try:
            product = UpdateProduct(self.get_repository(), self.get_clock()).execute(
                command
            )
        except (ProductNotFound, AuditUserRequired, AuditUserNotFound) as error:
            self._raise_api_error(error)
        return Response(ProductSerializer(product).data)

    @action(detail=True, methods=["post"], url_path="delete", url_name="delete")
    def soft_delete(self, request, pk=None):
        command = DeleteProductCommand(
            product_id=pk,
            deleted_by=request.data.get("deleted_by"),
        )
        try:
            product = DeleteProduct(self.get_repository(), self.get_clock()).execute(
                command
            )
        except ProductNotFound as error:
            self._raise_api_error(error)
        except AuditUserRequired as error:
            return Response(
                {error.field_name: "Este campo es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except AuditUserNotFound as error:
            return Response(
                {error.field_name: "El usuario indicado no existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(DeletedProductSerializer(product).data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        query = ListProductsQuery(active_only=True, ordering=("-created_at",))
        products = ListProducts(self.get_repository()).execute(query)
        return Response(ProductSerializer(products, many=True).data)
