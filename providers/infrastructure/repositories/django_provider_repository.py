from django.db import transaction
from django.db.models import Q

from providers.domain.entities import Provider as ProviderEntity
from providers.domain.exceptions import ProviderNotFound
from providers.models import Provider as ProviderModel


class DjangoProviderRepository:
    """Django ORM persistence adapter for the Provider port."""

    related_fields = (
        "type",
        "company_bank",
        "bank_account_type",
        "dispatch_district",
        "dispatch_region",
    )

    relation_fields = {
        "type",
        "company_bank",
        "bank_account_type",
        "dispatch_district",
        "dispatch_region",
        "created_by",
        "confirmed_by",
        "updated_by",
        "deleted_by",
    }

    persisted_fields = (
        "code",
        "provider",
        "type",
        "rating",
        "obs_provider",
        "contact_name",
        "contact_mail",
        "contact_phone",
        "contact_phone2",
        "website_url",
        "obs_contact",
        "company_name",
        "company_rut",
        "company_activity",
        "legal_representative",
        "billing_address",
        "billing_mail",
        "billing_phone",
        "company_bank",
        "bank_account_type",
        "bank_account_number",
        "bank_account_mail",
        "dispatch_address",
        "dispatch_maps_location",
        "obs_dispatch",
        "dispatch_district",
        "dispatch_region",
        "is_active",
        "is_deleted",
        "is_confirmed",
        "created_by",
        "confirmed_by",
        "updated_by",
        "deleted_by",
        "log",
        "version",
    )

    def _queryset(self):
        return ProviderModel.objects.select_related(*self.related_fields)

    @staticmethod
    def _related_value(model, relation_name, attribute_name):
        relation = getattr(model, relation_name)
        return getattr(relation, attribute_name) if relation is not None else None

    @classmethod
    def _to_entity(cls, model):
        return ProviderEntity(
            id=model.id,
            code=model.code,
            provider=model.provider,
            type=model.type_id,
            type_name=model.type.type,
            rating=model.rating,
            obs_provider=model.obs_provider,
            contact_name=model.contact_name,
            contact_mail=model.contact_mail,
            contact_phone=model.contact_phone,
            contact_phone2=model.contact_phone2,
            website_url=model.website_url,
            obs_contact=model.obs_contact,
            company_name=model.company_name,
            company_rut=model.company_rut,
            company_activity=model.company_activity,
            legal_representative=model.legal_representative,
            billing_address=model.billing_address,
            billing_mail=model.billing_mail,
            billing_phone=model.billing_phone,
            company_bank=model.company_bank_id,
            bank_name=cls._related_value(model, "company_bank", "bank"),
            bank_account_type=model.bank_account_type_id,
            bank_account_type_name=cls._related_value(
                model,
                "bank_account_type",
                "type",
            ),
            bank_account_number=model.bank_account_number,
            bank_account_mail=model.bank_account_mail,
            dispatch_address=model.dispatch_address,
            dispatch_maps_location=model.dispatch_maps_location,
            obs_dispatch=model.obs_dispatch,
            dispatch_district=model.dispatch_district_id,
            dispatch_district_name=cls._related_value(
                model,
                "dispatch_district",
                "district",
            ),
            dispatch_region=model.dispatch_region_id,
            dispatch_region_name=cls._related_value(
                model,
                "dispatch_region",
                "region",
            ),
            is_active=model.is_active,
            is_deleted=model.is_deleted,
            is_confirmed=model.is_confirmed,
            created_at=model.created_at,
            updated_at=model.updated_at,
            confirmed_at=model.confirmed_at,
            deleted_at=model.deleted_at,
            created_by=model.created_by_id,
            confirmed_by=model.confirmed_by_id,
            updated_by=model.updated_by_id,
            deleted_by=model.deleted_by_id,
            log=model.log,
            version=model.version,
        )

    def get(self, provider_id):
        try:
            model = self._queryset().get(pk=provider_id)
        except ProviderModel.DoesNotExist as error:
            raise ProviderNotFound from error
        return self._to_entity(model)

    def list(self, filters, search, ordering):
        queryset = self._queryset()
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(provider__icontains=search)
                | Q(contact_name__icontains=search)
                | Q(company_name__icontains=search)
                | Q(contact_mail__icontains=search)
            )
        queryset = queryset.order_by(*ordering)
        return [self._to_entity(model) for model in queryset]

    @classmethod
    def _persistence_values(cls, provider, fields):
        values = {}
        for field_name in fields:
            key = f"{field_name}_id" if field_name in cls.relation_fields else field_name
            values[key] = getattr(provider, field_name)
        return values

    @transaction.atomic
    def create(self, provider):
        values = self._persistence_values(provider, self.persisted_fields)
        model = ProviderModel.objects.create(**values)
        return self.get(model.pk)

    @transaction.atomic
    def update(self, provider, changed_fields):
        # Preserve the model's existing normalization behavior.
        if not provider.is_confirmed:
            provider.is_confirmed = False
        changed_fields.add("is_confirmed")
        values = self._persistence_values(provider, changed_fields)
        updated = ProviderModel.objects.filter(pk=provider.id).update(**values)
        if not updated:
            raise ProviderNotFound
        return self.get(provider.id)

    @transaction.atomic
    def delete(self, provider_id):
        try:
            provider = ProviderModel.objects.get(pk=provider_id)
        except ProviderModel.DoesNotExist as error:
            raise ProviderNotFound from error
        provider.delete()
