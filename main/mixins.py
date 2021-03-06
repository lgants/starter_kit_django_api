from django.db.models import Model
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from typing import Any, Optional
from .permissions import AllowAny
from django.core.exceptions import ValidationError, PermissionDenied


class AuthType:
    """
    Permission mixin for queries (types).
    Allows for simple configuration of access to types via class system.
    """
    permission_classes = (AllowAny,)

    @classmethod
    def resolve(cls, info: ResolveInfo, id: str) -> Optional[Model]:
        if all((perm().has_type_permission(info, id) for perm in cls.permission_classes)):
            try:
                object_instance = cls._meta.model.objects.get(id=id)  # type: ignore
            except cls._meta.model.DoesNotExist:  # type: ignore
                object_instance = None
            return object_instance
        else:
            raise PermissionDenied('Permission Denied.')


class AuthMutation:
    """
    Permission mixin for ClientIdMutation.
    """
    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        permitted = all(
            (perm().has_mutation_permission(root, info, input) for perm in cls.permission_classes)
        )

        if permitted:
            return True
        else:
            raise PermissionDenied('Permission Denied.')


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for permission system.
    """
    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        permitted = all(
            (perm().has_filter_permission(info) for perm in cls.permission_classes)
        )

        if permitted:
            return True
        else:
            raise PermissionDenied('Permission Denied.')

    @classmethod
    def connection_resolver(
        cls, resolver, connection, default_manager,
        max_limit, enforce_first_or_last, filterset_class,
        filtering_args, root, info, **args
    ):

        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(
            data=filter_kwargs,
            queryset=default_manager.get_queryset()
        ).qs

        if not cls.has_permission(info):
            return super(DjangoFilterConnectionField, cls).connection_resolver(
                resolver, connection, qs.none(), max_limit, enforce_first_or_last,
                root, info, **args,
            )

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver, connection, qs, max_limit, enforce_first_or_last,
            filterset_class, filtering_args, **args,
        )
