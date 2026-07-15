from django.db import transaction
from django.db.models import Q

from products.domain.entities import Product as ProductEntity
from products.domain.exceptions import ProductNotFound
from products.models import Product as ProductModel
from users.models import User


class DjangoProductRepository:
    """Django ORM persistence adapter for the Product port."""

    related_fields = (
        "price",
        "provider",
        "type",
        "item_group",
        "category",
        "package",
    )

    def _base_queryset(self):
        return ProductModel.objects.select_related(*self.related_fields).filter(
            Q(is_deleted=False) | Q(is_deleted__isnull=True)
        )

    @staticmethod
    def _to_entity(model):
        return ProductEntity(
            id=model.id,
            code=model.code,
            sku=model.sku,
            description=model.description,
            obs=model.obs,
            package_unit=model.package_unit,
            min_package_purchase=model.min_package_purchase,
            price=model.price_id,
            price_gross_amount=model.price.gross_amount,
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

    def get(self, product_id):
        try:
            model = self._base_queryset().get(pk=product_id)
        except ProductModel.DoesNotExist as error:
            raise ProductNotFound from error
        return self._to_entity(model)

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
        queryset = queryset.order_by(*ordering)
        return [self._to_entity(model) for model in queryset]

    @transaction.atomic
    def create(self, product):
        model = ProductModel.objects.create(
            code=product.code,
            sku=product.sku,
            description=product.description,
            obs=product.obs,
            package_unit=product.package_unit,
            min_package_purchase=product.min_package_purchase,
            price_id=product.price,
            provider_id=product.provider,
            type_id=product.type,
            item_group_id=product.item_group,
            category_id=product.category,
            package_id=product.package,
            url=product.url,
            is_active=product.is_active,
            is_deleted=product.is_deleted,
            is_confirmed=product.is_confirmed,
            created_at=product.created_at,
            created_by_id=product.created_by,
            confirmed_by_id=product.confirmed_by,
            updated_by_id=product.updated_by,
            log=product.log,
            version=product.version,
        )
        return self.get(model.pk)

    @transaction.atomic
    def update(self, product, changed_fields):
        relation_fields = {
            "price",
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
            values[key] = getattr(product, field_name)

        updated = self._base_queryset().filter(pk=product.id).update(**values)
        if not updated:
            raise ProductNotFound
        return self.get(product.id)

    @transaction.atomic
    def soft_delete(self, product):
        updated = self._base_queryset().filter(pk=product.id).update(
            is_active=product.is_active,
            is_deleted=product.is_deleted,
            deleted_at=product.deleted_at,
            deleted_by_id=product.deleted_by,
            log=product.log,
        )
        if not updated:
            raise ProductNotFound

        # Deleted rows are intentionally excluded from get/base queryset.
        model = ProductModel.objects.select_related(*self.related_fields).get(
            pk=product.id
        )
        return self._to_entity(model)

    def user_exists(self, user_code):
        return User.objects.filter(code=user_code).exists()
