"""Модуль настройки приложения Recipes."""

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Настройки приложения Recipes."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
