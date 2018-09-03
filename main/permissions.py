from graphql import ResolveInfo
from typing import Any
from django.contrib.auth import get_user_model
from .helpers import get_object
# https://github.com/redzej/graphene-permissions

User = get_user_model()

class AllowAny:
    """
    Default authentication class.
    Allows any user for any action.
    Subclass it and override methods below.
    """

    @staticmethod
    def has_type_permission(info: ResolveInfo, id: str) -> bool:
        return True

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return True

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return True


class AllowAuthenticated:
    """
    Allows performing action only for logged in users.
    """

    @staticmethod
    def has_type_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_authenticated


class AllowStaff:
    """
    Allow performing action only for staff users.
    """

    @staticmethod
    def has_type_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_staff


class AllowSuperuser:
    """
    Allow performing action only for superusers.
    """

    @staticmethod
    def has_type_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_superuser


class AllowOwnerOrSuperuser:
    """
    Allow performing action only by instance owner.
    """

    @staticmethod
    def has_type_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        user = info.context.user
        mutation_input = input.get('input', {})
        instance = get_object(root, mutation_input.get('id'), root())

        if isinstance(instance, User):
            return user.is_superuser or user == instance
        else:
            return user.is_superuser or user == instance.user

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_superuser
