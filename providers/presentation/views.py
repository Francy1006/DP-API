from types import SimpleNamespace

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from providers.application.commands import (
    CreateProviderCommand,
    ListProvidersQuery,
    UpdateProviderCommand,
)
from providers.application.use_cases import (
    CreateProvider,
    DeleteProvider,
    GetProvider,
    ListProviders,
    UpdateProvider,
)
from providers.domain.exceptions import ProviderNotFound
from providers.infrastructure.repositories import DjangoProviderRepository
from providers.presentation.serializers import (
    ProviderCommandSerializer,
    ProviderFilterSerializer,
    ProviderSerializer,
)


RELATION_VALUE_FIELDS = {
    "type": "pk",
    "company_bank": "pk",
    "bank_account_type": "pk",
    "dispatch_district": "pk",
    "dispatch_region": "pk",
    "created_by": "code",
    "confirmed_by": "code",
    "updated_by": "code",
    "deleted_by": "code",
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


class ProviderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """REST adapter delegating Provider operations to application use cases."""

    serializer_class = ProviderCommandSerializer
    filter_fields = (
        "type",
        "is_active",
        "is_deleted",
        "is_confirmed",
        "dispatch_region",
        "dispatch_district",
    )
    ordering_fields = {"provider", "rating", "created_at"}

    def get_repository(self):
        return DjangoProviderRepository()

    @staticmethod
    def _raise_not_found(error):
        if isinstance(error, ProviderNotFound):
            raise NotFound
        raise error

    def _get_provider(self, provider_id):
        try:
            return GetProvider(self.get_repository()).execute(provider_id)
        except ProviderNotFound as error:
            self._raise_not_found(error)

    def _query_from_request(self, request, extra_filters=None):
        filter_data = {
            name: request.query_params[name]
            for name in self.filter_fields
            if name in request.query_params
        }
        if extra_filters:
            filter_data.update(extra_filters)
        filter_serializer = ProviderFilterSerializer(data=filter_data)
        filter_serializer.is_valid(raise_exception=True)

        ordering = []
        requested_ordering = request.query_params.get("ordering", "provider")
        for field_name in requested_ordering.split(","):
            if field_name.lstrip("-") in self.ordering_fields:
                ordering.append(field_name)
        if not ordering:
            ordering = ["provider"]

        return ListProvidersQuery(
            filters=filter_serializer.validated_data,
            search=request.query_params.get("search") or None,
            ordering=tuple(ordering),
        )

    def list(self, request, *args, **kwargs):
        providers = ListProviders(self.get_repository()).execute(
            self._query_from_request(request)
        )
        page = self.paginate_queryset(providers)
        if page is not None:
            data = ProviderSerializer(page, many=True).data
            return self.get_paginated_response(data)
        return Response(ProviderSerializer(providers, many=True).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        provider = self._get_provider(pk)
        return Response(ProviderSerializer(provider).data)

    def create(self, request, *args, **kwargs):
        serializer = ProviderCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = CreateProviderCommand(
            data=_primitive_values(serializer.validated_data)
        )
        provider = CreateProvider(self.get_repository()).execute(command)
        response_data = ProviderSerializer(provider).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(response_data),
        )

    def _update(self, request, pk, partial):
        current = self._get_provider(pk)
        serializer = ProviderCommandSerializer(
            instance=SimpleNamespace(pk=current.id),
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        command = UpdateProviderCommand(
            provider_id=current.id,
            changes=_primitive_values(serializer.validated_data),
        )
        try:
            provider = UpdateProvider(self.get_repository()).execute(command)
        except ProviderNotFound as error:
            self._raise_not_found(error)
        return Response(ProviderSerializer(provider).data)

    def update(self, request, pk=None, *args, **kwargs):
        return self._update(request, pk, partial=False)

    def partial_update(self, request, pk=None, *args, **kwargs):
        return self._update(request, pk, partial=True)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            DeleteProvider(self.get_repository()).execute(pk)
        except ProviderNotFound as error:
            self._raise_not_found(error)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def active(self, request):
        query = ListProvidersQuery(
            filters={"is_active": True, "is_deleted": False},
        )
        providers = ListProviders(self.get_repository()).execute(query)
        return Response(ProviderSerializer(providers, many=True).data)

    @action(detail=False, methods=["get"])
    def confirmed(self, request):
        query = ListProvidersQuery(
            filters={"is_confirmed": True, "is_deleted": False},
        )
        providers = ListProviders(self.get_repository()).execute(query)
        return Response(ProviderSerializer(providers, many=True).data)

    @action(detail=False, methods=["get"])
    def by_type(self, request):
        type_id = request.query_params.get("type_id")
        if not type_id:
            return Response(
                {"error": "type_id parameter required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        query = ListProvidersQuery(
            filters={"type": type_id, "is_deleted": False},
        )
        providers = ListProviders(self.get_repository()).execute(query)
        return Response(ProviderSerializer(providers, many=True).data)
