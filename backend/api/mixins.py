"""Модуль вьюсетов для приложения Api."""

from rest_framework import status, viewsets
from rest_framework.response import Response


class NotPutModelViewSet(viewsets.ModelViewSet):
    """Вьюсет для моделей с запретом PUT-запросов."""

    def update(self, request, *args, **kwargs):
        """PUT-запросы запрещены."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
