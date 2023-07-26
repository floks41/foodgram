"""Модуль фильтров для представлений приложения Api."""

from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
    NumberFilter,
)

from recipes.models import Recipe, Tag
from users.models import User


class IngredientFilter(FilterSet):
    """Фильтр для ингредиентов."""

    name = CharFilter(field_name='name', lookup_expr='istartswith')


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""

    author = NumberFilter(field_name='author', lookup_expr='exact')

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug', to_field_name='slug', queryset=Tag.objects.all()
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')

    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        user: User = self.request.user
        if not user.is_anonymous and value:
            return queryset.filter(favorite_recipes__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user: User = self.request.user
        if not user.is_anonymous and value:
            return queryset.filter(shopping_cart_recipes__user=user)
        return queryset
