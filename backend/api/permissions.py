"""Модуль разрешений для представлений приложения Api."""


from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAuthorOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только автору.

    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    """

    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только администратору.

    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    """

    def has_permission(self, request, view):
        user: User = request.user
        return request.method in SAFE_METHODS or (
            user.is_authenticated and user.is_staff and user.is_superuser
        )
