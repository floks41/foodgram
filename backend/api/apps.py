"""Модуль настройки приложения Api."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Настройки приложения Api."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
