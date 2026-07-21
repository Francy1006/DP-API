from types import SimpleNamespace

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.response import Response

from pricing.domain.exceptions import (
    InvalidBaseNetAmount,
    MaterialPriceConfigurationUnavailable,
    PricingError,
)
from pricing.infrastructure.repositories import DjangoMaterialPriceRepository
from pricing.infrastructure.transactions import DjangoTransactionManager
from products.application.material_commands import (
    CreateMaterialCommand,
    DeleteMaterialCommand,
    ListMaterialsQuery,
    UpdateMaterialCommand,
)
from products.application.use_cases.material import (
    CreateMaterial,
    DeleteMaterial,
    GetMaterial,
    ListMaterials,
    UpdateMaterial,
)
from products.domain.material_exceptions import (
    ImmutableMaterialField,
    LegacyMaterialPriceInputRequired,
    MaterialAuditUserNotFound,
    MaterialAuditUserRequired,
    MaterialNotFound,
)
from products.infrastructure.clock import DjangoClock
from products.infrastructure.repositories import DjangoMaterialRepository
from products.presentation.material_serializers import (
    DeletedMaterialSerializer,
    MaterialCommandSerializer,
    MaterialFilterSerializer,
    MaterialSerializer,
)


class MaterialPriceVersionConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "material_price_version_conflict"
    default_detail = {
        "base_net_amount": [
            "El precio vigente del material no puede versionarse de forma segura."
        ]
    }


RELATION_VALUE_FIELDS = {
    "provider": "pk",
    "type": "pk",
    "item_group": "pk",
    "category": "pk",
    "package": "pk",
    "created_by": "code",
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


class MaterialViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MaterialCommandSerializer
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
        return DjangoMaterialRepository()

    def get_clock(self):
        return DjangoClock()

    @staticmethod
    def _raise_api_error(error):
        if isinstance(error, MaterialNotFound):
            raise NotFound
        if isinstance(error, MaterialAuditUserRequired):
            raise ValidationError({error.field_name: "Este campo es requerido."})
        if isinstance(error, MaterialAuditUserNotFound):
            raise ValidationError(
                {error.field_name: "El usuario indicado no existe."}
            )
        if isinstance(error, ImmutableMaterialField):
            raise ValidationError(
                {error.field_name: "Este campo no puede modificarse."}
            )
        if isinstance(error, LegacyMaterialPriceInputRequired):
            raise ValidationError(
                {
                    field_name: (
                        "Este campo es requerido para crear el precio del material legacy."
                    )
                    for field_name in error.missing_fields
                }
            )
        if isinstance(error, InvalidBaseNetAmount):
            raise ValidationError(
                {"base_net_amount": "Debe ser un decimal mayor que 0."}
            )
        if isinstance(error, MaterialPriceConfigurationUnavailable):
            raise ValidationError(
                {
                    "price_configuration": (
                        "La configuración no está disponible para precios de material."
                    )
                }
            )
        if isinstance(error, PricingError):
            raise MaterialPriceVersionConflict
        raise error

    def _get_material(self, material_id):
        try:
            return GetMaterial(self.get_repository()).execute(material_id)
        except MaterialNotFound as error:
            self._raise_api_error(error)

    def list(self, request, *args, **kwargs):
        filter_serializer = MaterialFilterSerializer(
            data={
                name: request.query_params[name]
                for name in self.filter_fields
                if name in request.query_params
            }
        )
        filter_serializer.is_valid(raise_exception=True)

        ordering = []
        for field_name in request.query_params.get(
            "ordering",
            "description",
        ).split(","):
            if field_name.lstrip("-") in self.ordering_fields:
                ordering.append(field_name)
        if not ordering:
            ordering = ["description"]

        query = ListMaterialsQuery(
            filters=filter_serializer.validated_data,
            search=request.query_params.get("search") or None,
            ordering=tuple(ordering),
        )
        materials = ListMaterials(self.get_repository()).execute(query)
        page = self.paginate_queryset(materials)
        if page is not None:
            return self.get_paginated_response(
                MaterialSerializer(page, many=True).data
            )
        return Response(MaterialSerializer(materials, many=True).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response(MaterialSerializer(self._get_material(pk)).data)

    def create(self, request, *args, **kwargs):
        serializer = MaterialCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = _primitive_values(serializer.validated_data)
        command = CreateMaterialCommand(
            code=values["code"],
            description=values["description"],
            obs=values["obs"],
            package_unit=values["package_unit"],
            min_package_purchase=values["min_package_purchase"],
            base_net_amount=values["base_net_amount"],
            price_configuration=values["price_configuration"],
            provider=values["provider"],
            type=values["type"],
            item_group=values["item_group"],
            category=values["category"],
            package=values["package"],
            created_by=values["created_by"],
            url=values.get("url"),
            is_active=values.get("is_active", True),
            is_confirmed=values.get("is_confirmed"),
            updated_by=values.get("updated_by"),
        )
        try:
            material = CreateMaterial(
                repository=self.get_repository(),
                price_repository=DjangoMaterialPriceRepository(),
                transaction_manager=DjangoTransactionManager(),
                clock=self.get_clock(),
            ).execute(command)
        except (MaterialNotFound, ImmutableMaterialField, PricingError) as error:
            self._raise_api_error(error)
        except (MaterialAuditUserRequired, MaterialAuditUserNotFound) as error:
            self._raise_api_error(error)

        response_data = MaterialSerializer(material).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(response_data),
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        current = self._get_material(pk)
        serializer = MaterialCommandSerializer(
            instance=SimpleNamespace(pk=current.id),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        values = _primitive_values(serializer.validated_data)
        updated_by = values.pop("updated_by", None)
        command = UpdateMaterialCommand(
            material_id=current.id,
            changes=values,
            updated_by=updated_by,
        )
        try:
            material = UpdateMaterial(
                repository=self.get_repository(),
                price_repository=DjangoMaterialPriceRepository(),
                transaction_manager=DjangoTransactionManager(),
                clock=self.get_clock(),
            ).execute(command)
        except (
            MaterialNotFound,
            MaterialAuditUserRequired,
            MaterialAuditUserNotFound,
            ImmutableMaterialField,
            LegacyMaterialPriceInputRequired,
            PricingError,
        ) as error:
            self._raise_api_error(error)
        return Response(MaterialSerializer(material).data)

    @action(detail=True, methods=["post"], url_path="delete", url_name="delete")
    def soft_delete(self, request, pk=None):
        command = DeleteMaterialCommand(
            material_id=pk,
            deleted_by=request.data.get("deleted_by"),
        )
        try:
            material = DeleteMaterial(
                self.get_repository(),
                self.get_clock(),
            ).execute(command)
        except (
            MaterialNotFound,
            MaterialAuditUserRequired,
            MaterialAuditUserNotFound,
        ) as error:
            self._raise_api_error(error)
        return Response(DeletedMaterialSerializer(material).data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        materials = ListMaterials(self.get_repository()).execute(
            ListMaterialsQuery(active_only=True, ordering=("-created_at",))
        )
        return Response(MaterialSerializer(materials, many=True).data)
