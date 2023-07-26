"""Настройки административной панели для моделей приложения Recipes."""

from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройки отображения модели Tag в административной панели."""

    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
        'slug',
    )
    search_fields = ('name__icontains',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройки отображения модели Ingredient в административной панели."""

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('measurement_unit',)
    search_fields = ('name__icontains',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Настройки отображения модели ShoppingCart в административной панели."""

    list_display = (
        'user',
        'recipe',
    )


@admin.register(Favorite)
class FavouriteAdmin(ShoppingCartAdmin):
    """Настройки отображения модели Favourite в административной панели."""

    pass


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


class RecipeTagsInLine(admin.TabularInline):
    """Настройка для отображения элементов редактирования
    связанной модели Tag для модели Recipe."""

    model = Recipe.tags.through
    extra = 1


class RecipeIngredientsInLine(admin.TabularInline):
    """Настройка для отображения элементов редактирования
    связанной модели Ingredients для модели Recipe."""

    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройки отображения модели Recipe в административной панели."""

    list_display = (
        'name',
        'author',
        'display_favorite_count',
    )
    list_filter = (
        'tags',
        'name',
        'author',
    )
    search_fields = (
        'name',
        'author',
    )
    inlines = (
        RecipeIngredientsInLine,
        RecipeTagsInLine,
    )

    @admin.display(description='Добавлено в избранное, раз.')
    def display_favorite_count(self, obj: Recipe):
        """Доополнительное поле, сколько раз рейцепт
        добавлен пользователями в избранное."""

        return obj.in_favorites.count()
