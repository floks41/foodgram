"""Модуль моделей приложения Recipes."""

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Tag(models.Model):
    """Модель Тег."""

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': _('Тег с указанным именем уже существует.'),
        },
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7,
        null=True,
        unique=True,
        error_messages={
            'unique': _('Тег с указанным цветом уже существует.'),
        },
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$', message='Некорректный слаг'
            )
        ],
        error_messages={
            'unique': _('Тег с указанным slug уже существует.'),
        },
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель Ингредиент."""

    name = models.CharField(
        verbose_name='Название', max_length=200, blank=False, null=False
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f'{self.name} ({self.measurement_unit}.)'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_measurement_unit',
            )
        ]


class Recipe(models.Model):
    """Модель Рецепт."""

    name = models.CharField(
        verbose_name='Название', max_length=200, blank=False, null=False
    )
    text = models.TextField(verbose_name='Описание', blank=False, null=False)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message=(
                    'Время приготовления не может быть меньше одной минуты'
                ),
            )
        ],
    )
    image = models.ImageField(
        upload_to='recipe/image/', null=True, default=None
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    tags = models.ManyToManyField(
        to=Tag, related_name='recipes', verbose_name='Теги рецепта'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты в рецепте',
    )
    in_shopping_cart = models.ManyToManyField(
        to=User, through='ShoppingCart', related_name='shopping_cart_recipes'
    )
    in_favorites = models.ManyToManyField(
        to=User, through='Favorite', related_name='favorite_recipes'
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        """Настройки модели Рецептеов."""

        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientInRecipe(models.Model):
    """Модель Ингредиент в рецепте."""

    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        blank=False,
        null=False,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        blank=False,
        null=False,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество не может быть меньше одной единицы',
            )
        ],
    )

    class Meta:
        """Настройки модели Ингредиентов в рецепте."""

        ordering = ('id',)
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class ShoppingCart(models.Model):
    """Модель Корзина покупок."""

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
    )

    class Meta:
        """Настройки модели Корзина покупок."""

        ordering = ('id',)
        verbose_name = 'Корзина для покупок'
        verbose_name_plural = 'Корзины для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_user_shopping_cart',
            )
        ]


class Favorite(models.Model):
    """Модель Избранное."""

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name='favorite_recipes'
    )

    class Meta:
        """Настройки модели Избранное."""

        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_recipe_in_favorites'
            )
        ]


class Subscription(models.Model):
    """Модель подписка на авторов рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribes',
        verbose_name='подписчик',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор',
        help_text='Автор рецепта',
    )

    class Meta:
        """Настройки модели подписок на авторов рецептов."""

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='users_cannot_subscribe_themselves',
            ),
        ]
