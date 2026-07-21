from django.db import transaction
from django.db.models import F, Q

from pricing.models import Price as PriceModel
from pricing.models import PriceConfiguration
from products.domain.material_entities import Material as MaterialEntity
from products.domain.material_exceptions import MaterialNotFound
from products.models import Material as MaterialModel
from users.models import User


class DjangoMaterialRepository:
    """Django persistence adapter preserving legacy dangling Price UUIDs."""

    related_fields = (
        "provider",
        "type",
        "item_group",
        "category",
        "package",
    )

    def _base_queryset(self):
        return MaterialModel.objects.select_related(*self.related_fields).filter(
            Q(is_deleted=False) | Q(is_deleted__isnull=True)
        )

    @staticmethod
    def _price_map(price_codes):
        codes = {code for code in price_codes if code}
        if not codes:
            return {}
        return {
            price.code: price
            for price in PriceModel.objects.filter(code__in=codes)
        }

    @staticmethod
    def _configuration_labels(prices):
        codes = {
            price.price_configuration
            for price in prices
            if price and price.price_configuration
        }
        if not codes:
            return {}
        return dict(
            PriceConfiguration.objects.filter(code__in=codes).values_list(
                "code",
                "price_configuration",
            )
        )

    @staticmethod
    def _to_entity(model, price=None, configuration_label=None):
        return MaterialEntity(
            id=model.id,
            code=model.code,
            sku=model.sku,
            description=model.description,
            obs=model.obs,
            package_unit=model.package_unit,
            min_package_purchase=model.min_package_purchase,
            price=model.price,
            base_net_amount=price.base_net_amount if price else None,
            net_amount=price.net_amount if price else None,
            gross_amount=price.gross_amount if price else None,
            iva_amount=price.iva_amount if price else None,
            aditional_tax_amount=price.aditional_tax_amount if price else None,
            retention_amount=price.retention_amount if price else None,
            price_configuration=price.price_configuration if price else None,
            price_configuration_label=configuration_label,
            provider=model.provider_id,
            provider_name=model.provider.provider,
            type=model.type_id,
            type_name=model.type.type,
            item_group=model.item_group_id,
            item_group_name=model.item_group.group_name,
            category=model.category_id,
            category_name=model.category.category,
            url=model.url,
            package=model.package_id,
            package_description=model.package.description,
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

    def _hydrate(self, models):
        models = list(models)
        prices = self._price_map(model.price for model in models)
        labels = self._configuration_labels(prices.values())
        return [
            self._to_entity(
                model,
                prices.get(model.price),
                labels.get(prices[model.price].price_configuration)
                if model.price in prices
                else None,
            )
            for model in models
        ]

    def get(self, material_id):
        try:
            model = self._base_queryset().get(pk=material_id)
        except MaterialModel.DoesNotExist as error:
            raise MaterialNotFound from error
        return self._hydrate([model])[0]

    def get_for_update(self, material_id):
        try:
            model = self._base_queryset().select_for_update().get(pk=material_id)
        except MaterialModel.DoesNotExist as error:
            raise MaterialNotFound from error
        return self._hydrate([model])[0]

    def list(self, filters, search, ordering, active_only=False):
        queryset = self._base_queryset()
        if active_only:
            queryset = queryset.filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search)
                | Q(sku__icontains=search)
                | Q(description__icontains=search)
            )
        return self._hydrate(queryset.order_by(*ordering))

    @transaction.atomic
    def create(self, material):
        values = dict(
            code=material.code,
            description=material.description,
            obs=material.obs,
            package_unit=material.package_unit,
            min_package_purchase=material.min_package_purchase,
            price=material.price,
            provider_id=material.provider,
            type_id=material.type,
            item_group_id=material.item_group,
            category_id=material.category,
            package_id=material.package,
            url=material.url,
            is_active=material.is_active,
            is_deleted=material.is_deleted,
            is_confirmed=material.is_confirmed,
            created_at=material.created_at,
            confirmed_at=material.confirmed_at,
            created_by_id=material.created_by,
            confirmed_by_id=material.confirmed_by,
            updated_by_id=material.updated_by,
            log=material.log,
            version=material.version,
        )
        if material.sku:
            values["sku"] = material.sku

        model = MaterialModel.objects.create(**values)
        return self.get(model.pk)

    @transaction.atomic
    def update(self, material, changed_fields):
        relation_fields = {
            "provider",
            "type",
            "item_group",
            "category",
            "package",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
        }
        values = {}
        for field_name in changed_fields:
            key = f"{field_name}_id" if field_name in relation_fields else field_name
            values[key] = (
                F("version") + 1
                if field_name == "version"
                else getattr(material, field_name)
            )

        updated = self._base_queryset().filter(pk=material.id).update(**values)
        if not updated:
            raise MaterialNotFound
        return self.get(material.id)

    @transaction.atomic
    def soft_delete(self, material):
        updated = self._base_queryset().filter(pk=material.id).update(
            is_active=material.is_active,
            is_deleted=material.is_deleted,
            deleted_at=material.deleted_at,
            deleted_by_id=material.deleted_by,
            log=material.log,
        )
        if not updated:
            raise MaterialNotFound

        model = MaterialModel.objects.select_related(*self.related_fields).get(
            pk=material.id
        )
        return self._hydrate([model])[0]

    def user_exists(self, user_code):
        return User.objects.filter(code=user_code).exists()
