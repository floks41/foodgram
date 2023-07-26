"""Модуль сериализаторов для приложения Api."""

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
)
from users.models import User
from users.serializers import DjoserUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте."""

    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    def get_name(self, obj: IngredientInRecipe):
        return obj.ingredient.name

    def get_measurement_unit(self, obj: IngredientInRecipe):
        return obj.ingredient.measurement_unit

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""

    author = DjoserUserSerializer(required=True, many=False)
    tags = TagSerializer(required=False, many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.ImageField()

    def get_ingredients(self, obj: Recipe):
        """Получает ингредиенты рецепта."""

        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        serializer = IngredientInRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj: Recipe):
        """Находится ли рецепт в избранном у текущего пользователя."""

        user: User = self.context.get('request').user
        return (
            not user.is_authenticated
            and Favorite.objects.filter(user=user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj: Recipe):
        """Находится ли рецепт в списке покупок у текущего пользователя."""

        user: User = self.context.get('request').user
        return (
            not user.is_authenticated
            and ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'image',
            'cooking_time',
            'author',
            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
        )


class IngredientInRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов рецепта для создания и обновления."""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для создания и обновления."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    ingredients = IngredientInRecipeCreateUpdateSerializer(many=True)
    author = DjoserUserSerializer(read_only=True)

    def set_ingredient_in_recipe_amount(self, ingredients, recipe):
        """Сохраняет значения для ингредиентов в рецепте при создании."""

        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    ingredient=get_object_or_404(
                        Ingredient, id=ingredient.get('id')
                    ),
                    recipe=recipe,
                    amount=ingredient.get('amount'),
                )
                for ingredient in ingredients
            ]
        )

    def set_ingredient_in_recipe_amount_for_update(
        self, ingredients_in_recipe, recipe
    ):
        """Сохраняет значения для ингредиентов в рецепте при обновлении."""

        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    ingredient=get_object_or_404(
                        Ingredient, id=ingredient.get('ingredient_id')
                    ),
                    recipe=recipe,
                    amount=ingredient.get('amount'),
                )
                for ingredient in ingredients_in_recipe
            ]
        )

    def create(self, validated_data):
        """Создание рецепта."""

        author = self.context.get('request').user
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.set_ingredient_in_recipe_amount(
            ingredients=ingredients, recipe=recipe
        )
        return recipe

    def update(self, instance: Recipe, validated_data):
        """Обновление рецепта."""

        tags = validated_data.pop('tags', None)
        ingredients_in_recipe = validated_data.pop('ingredients', None)
        for item in ingredients_in_recipe:
            if IngredientInRecipe.objects.filter(pk=item.get('id')).exists():
                item['ingredient_id'] = get_object_or_404(
                    IngredientInRecipe, pk=item.get('id')
                ).ingredient.pk
            else:
                item['ingredient_id'] = item.get('id')
        instance = super().update(
            instance=instance, validated_data=validated_data
        )
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.set_ingredient_in_recipe_amount_for_update(
            recipe=instance, ingredients_in_recipe=ingredients_in_recipe
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        """Возвращает отображение рецепта после создания или обновления."""

        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance=instance, context=context).data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'image',
            'cooking_time',
            'author',
            'tags',
            'ingredients',
        )


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Сеериалиатор рецепта для краткого отображения."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ChosenCreateAbstractSerializer(serializers.ModelSerializer):
    """Абстрактный сериалиатор для создания подборок
    (избранное и корзина для покупок).
    В мета-подклассе наследника необходимо определить модель.
    """

    def validate(self, data):
        """Проверяет на наличие рецепта в подборке."""

        if self.Meta.model.objects.filter(**data).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в подборку.'
            )
        return data

    class Meta:
        fields = ('user', 'recipe')


class ChosenDeleteAbstractSerializer(ChosenCreateAbstractSerializer):
    """Абстрактный сериалиатор для удаления подборок
    (избранное и корзина для покупок).
    В мета-подклассе наследника необходимо определить модель.
    """

    def validate(self, data):
        """Проверяет на наличие рецепта в подборке.
        Находит объект модели в базе данных,
        устанавливает в instance сериализатора перед удалением.
        """

        if not self.Meta.model.objects.filter(**data).exists():
            raise serializers.ValidationError('Запись отсутствует.')
        self.instance = self.Meta.model.objects.get(**data)

        return data

    class Meta(ChosenCreateAbstractSerializer.Meta):
        pass


class FavoriteCreateSerializer(ChosenCreateAbstractSerializer):
    """Сериалиатор избранного для создания записи."""

    class Meta(ChosenCreateAbstractSerializer.Meta):
        model = Favorite


class FavoriteDeleteSerializer(ChosenDeleteAbstractSerializer):
    """Сериалиатор подборки (избранного) для удаления записи."""

    class Meta(ChosenDeleteAbstractSerializer.Meta):
        model = Favorite


class ShoppingCartCreateSerializer(ChosenCreateAbstractSerializer):
    """Сериалиатор подборки (корзина для покупок) для создания записи."""

    class Meta(ChosenCreateAbstractSerializer.Meta):
        model = ShoppingCart


class ShoppingCartDeleteSerializer(ChosenDeleteAbstractSerializer):
    """Сериалиатор подборки (корзина для покупок) для удаления записи."""

    class Meta(ChosenDeleteAbstractSerializer.Meta):
        model = ShoppingCart


class SubscriptionDeleteSerializer(ChosenDeleteAbstractSerializer):
    """Cериализатор удаления для подписок."""

    class Meta:
        model = Subscription
        fields = ('user', 'author')


class SubscriptionCreateSerializer(SubscriptionDeleteSerializer):
    """Сериализатор создания подписки."""

    def validate(self, data):
        """Проверяет на наличие уже существующей подписки,
        и исключает подписку на самого себя."""

        if self.Meta.model.objects.filter(**data).exists():
            raise serializers.ValidationError('Подписка уже существует.')
        if data.get('user') == data.get('author'):
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена.'
            )
        return data

    class Meta(SubscriptionDeleteSerializer.Meta):
        pass


class UserWithRecipesSerializer(DjoserUserSerializer):
    """Сериализатор для пользователей с рецептами.

    Использует параметр get-запроса recipes_limit,
    который перадается через контекст.
    """

    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')

    def get_recipes(self, obj: User):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')

        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = RecipeMinifiedSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj: User):
        return obj.recipes.count()

    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
        write_only_fields = (
            'username',
            'email',
            'password',
        )
