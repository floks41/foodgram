"""Модуль представлений для приложения Api."""


from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import NotPutModelViewSet
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    FavoriteCreateSerializer,
    FavoriteDeleteSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeMinifiedSerializer,
    RecipeReadSerializer,
    ShoppingCartCreateSerializer,
    ShoppingCartDeleteSerializer,
    SubscriptionCreateSerializer,
    SubscriptionDeleteSerializer,
    TagSerializer,
    UserWithRecipesSerializer,
)
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class RecipeViewSet(NotPutModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [
        (IsAdminOrReadOnly | IsAuthorOrReadOnly),
    ]

    def get_serializer_class(self):
        """возвражает класс-сериализатор в зависимости от метода запроса."""

        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateUpdateSerializer

    def get_chosen_data(self) -> dict:
        """Формирует данные для сериализатора подборки."""

        return {'user': self.request.user.pk, 'recipe': self.kwargs.get('pk')}

    def get_serializer_for_chosen(self, serializer_class):
        """Вовращает экземпляр сериализатора подборки."""

        return serializer_class(data=self.get_chosen_data())

    def get_chosen_instance(self, serializer_class):
        """Возвращает экземспляр объекта подборки из сериализатора."""

        serializer = serializer_class(data=self.get_chosen_data())
        serializer.is_valid(raise_exception=True)
        if serializer.instance:
            return serializer.instance
        return serializer.save()

    def get_chosen_recipe_data(self, chosen_instance):
        """Возвращает данные рецепта в сокращенном виде."""

        recipe_serializer = RecipeMinifiedSerializer(chosen_instance.recipe)
        return recipe_serializer.data

    def chosen_action(self, create_serializer_class, delete_serializer_class):
        """Исполняет действия с подборкой.

        Создание и удаление избранного и корзины для покупок."""

        if self.request.method == 'POST':
            data = self.get_chosen_recipe_data(
                self.get_chosen_instance(create_serializer_class)
            )

            return Response(data, status=status.HTTP_201_CREATED)

        instance = self.get_chosen_instance(delete_serializer_class)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['POST', 'DELETE'],
        url_path=r'(?P<pk>\d+)/favorite',
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def favorite(self, request, **kwargs):
        """Избранное добавить-удалить."""

        return self.chosen_action(FavoriteCreateSerializer, FavoriteDeleteSerializer)

    @action(
        detail=False,
        methods=['POST', 'DELETE'],
        url_path=r'(?P<pk>\d+)/shopping_cart',
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, **kwargs):
        """Корзина для покупок добавить-удалить."""

        return self.chosen_action(
            ShoppingCartCreateSerializer, ShoppingCartDeleteSerializer
        )

    def make_shopping_cart_text_string(self, ingredient_in_cart: dict) -> str:
        """Формирует текстовую строку со списком покупок."""

        response_string = 'Список покупок\n'
        response_string += ''.join(
            [
                (
                    f"\n\u00B7 {str(item.get('name')).capitalize()} "
                    f"({item.get('measurement_unit')}.) "
                    f"\u2014 {item.get('amount')}"
                )
                for item in ingredient_in_cart
            ]
        )

        response_string += '\n\n\u00A9 Foodgram  \u2122. 2023.'
        return response_string

    @action(
        detail=False,
        methods=[
            'GET',
        ],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def download_shopping_cart(self, request, **kwargs):
        """Загрузить текстовый файл со списком покупок."""

        ingredient_in_cart = (
            Ingredient.objects.filter(recipes__shopping_cart_recipes__user=request.user)
            .values('name', 'measurement_unit')
            .annotate(amount=Sum('recipe__amount'))
        )

        file_name = 'shopping_list.txt'

        return HttpResponse(
            self.make_shopping_cart_text_string(ingredient_in_cart),
            headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': f'attachment; filename={file_name}',
            },
        )


class UserSubscriptionsViewSet(viewsets.GenericViewSet):
    """Вьюсет для подписок."""

    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def check_author_existenсe(self):
        """Проверка входных данных из path-параметров запроса."""

        if not User.objects.filter(pk=self.kwargs.get('pk')).exists():
            raise NotFound('Автор не найден.')

    def get_subscription_data(self) -> dict:
        """Возвращает данные для сериализатора подписки."""
        self.check_author_existenсe()
        return {'user': self.request.user.pk, 'author': self.kwargs.get('pk')}

    def get_context(self) -> dict:
        """Возвращает контекст запроса для передачи в сериализатор,
        где используется параметр recipe_limit."""

        return {'request': self.request}

    @action(detail=False, methods=['POST', 'DELETE'], url_path=r'(?P<pk>\d+)/subscribe')
    def subscribe(self, request, **kwargs):
        """Подписка добавить-удалить."""

        if request.method == 'POST':
            serializer = SubscriptionCreateSerializer(data=self.get_subscription_data())

            if serializer.is_valid(raise_exception=True):
                subscription = serializer.save()
                subscription_serializer = UserWithRecipesSerializer(
                    instance=subscription.author, context=self.get_context()
                )

                return Response(
                    data=subscription_serializer.data, status=status.HTTP_201_CREATED
                )

        serializer = SubscriptionDeleteSerializer(data=self.get_subscription_data())
        serializer.is_valid(raise_exception=True)
        instance = serializer.instance
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=[
            'GET',
        ],
    )
    def subscriptions(self, request, **kwargs):
        """Список подписок."""

        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
