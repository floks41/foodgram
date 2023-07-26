"""Модуль административной команды загрузки тестовых данных."""

from csv import DictReader

from django.core.files import File
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import User

PATH = './data/'
MESSAGE = 'был успешно загружен в базу данных.'
UTF = 'UTF-8'

INGREDIENT = 'ingredients.csv'
INGREDIENT_FIELDS = ('name', 'measurement_unit')
USERS = 'users.csv'
TAGS = 'tags.csv'
RECIPES = 'recipes.csv'
RECIPE_TAGS = 'recipe_tags.csv'
INGREDIENT_IN_RECIPE = 'ingredient_in_recipes.csv'
FAVORITES = 'favorites.csv'
SHOPPING_CARTS = 'shopping_carts.csv'
RECIPE_IMAGES_PATH = './data/pics/'

RECIPE_IMAGES = {
    '1': 'borsch.jpg',
    '2': 'uha.jpg',
    '3': 'kotlet.jpg',
    '4': 'oladi.jpg',
    '5': 'blini.jpg',
    '6': 'sharlotka.jpg',
    '7': 'rapans.jpg',
    '8': 'kartzap.jpg',
    '9': 'zhul.jpg',
    '10': 'kurovosch.jpg',
    '11': 'kurkot.jpg',
    '12': 'omlet.jpg',
}


class Command(BaseCommand):
    """Административная команда для загрузки тестовых данных."""

    help = (
        'Загружает тестовые данные из csv файлов и изображения в базу '
        'данных проекта. До их загрузки должен быть создан один '
        'пользователь.'
    )

    def load_ingredient(self):
        """Загрузка ингредиентов."""

        for row in DictReader(
            f=open(f'{PATH}{INGREDIENT}', encoding=UTF), fieldnames=INGREDIENT_FIELDS
        ):
            Ingredient.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f'{INGREDIENT} {MESSAGE}'))

    def load_users(self):
        """Загрузка пользователей."""

        for row in DictReader(f=open(f'{PATH}{USERS}', encoding=UTF)):
            User.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f'{USERS} {MESSAGE}'))

    def load_tags(self):
        """Загрузка тегов."""

        for row in DictReader(f=open(f'{PATH}{TAGS}', encoding=UTF)):
            Tag.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f'{TAGS} {MESSAGE}'))

    def load_recipes(self):
        """Загрузка рецептов."""

        for row in DictReader(f=open(f'{PATH}{RECIPES}', encoding=UTF)):
            Recipe.objects.get_or_create(
                author=User.objects.get(pk=row.pop('author_id')), **row
            )
        self.stdout.write(self.style.SUCCESS(f'{RECIPES} {MESSAGE}'))

    def load_recipe_tags(self):
        """Загрузка тегов рецептов."""

        for row in DictReader(f=open(f'{PATH}{RECIPE_TAGS}', encoding=UTF)):
            Recipe.objects.get(id=row.get('recipe_id')).tags.add(row.get('tag_id'))
        self.stdout.write(self.style.SUCCESS(f'{RECIPE_TAGS} {MESSAGE}'))

    def load_ingredient_in_recipe(self):
        """Загрузка ингредиентов рецептов."""

        for row in DictReader(f=open(f'{PATH}{INGREDIENT_IN_RECIPE}', encoding=UTF)):
            IngredientInRecipe.objects.get_or_create(
                recipe=Recipe.objects.get(id=row.pop('recipe_id')),
                ingredient=Ingredient.objects.get(id=row.pop('ingredient_id')),
                **row,
            )
        self.stdout.write(self.style.SUCCESS(f'{INGREDIENT_IN_RECIPE} {MESSAGE}'))

    def load_favorites(self):
        """Загрузка избранного."""

        for row in DictReader(f=open(f'{PATH}{FAVORITES}', encoding=UTF)):
            Favorite.objects.get_or_create(
                recipe=Recipe.objects.get(id=row.pop('recipe_id')),
                user=User.objects.get(id=row.pop('user_id')),
            )
        self.stdout.write(self.style.SUCCESS(f'{FAVORITES} {MESSAGE}'))

    def load_shopping_carts(self):
        """Загрузка корзины для покупок."""

        for row in DictReader(f=open(f'{PATH}{SHOPPING_CARTS}', encoding=UTF)):
            ShoppingCart.objects.get_or_create(
                recipe=Recipe.objects.get(id=row.pop('recipe_id')),
                user=User.objects.get(id=row.pop('user_id')),
            )
        self.stdout.write(self.style.SUCCESS(f'{SHOPPING_CARTS} {MESSAGE}'))

    def load_recipe_images(self):
        """Загрузка изображений рецептов."""

        for id, file_name in RECIPE_IMAGES.items():
            f = open(f'{RECIPE_IMAGES_PATH}{file_name}', mode='rb')
            image_file = File(f)
            recipe = Recipe.objects.get(id=id)
            recipe.image.save(file_name, image_file, save=True)
            self.stdout.write(
                self.style.SUCCESS(f'{RECIPE_IMAGES_PATH}{file_name} {MESSAGE}')
            )

    def handle(self, *args, **options):
        """Исполнение административной команды."""

        try:
            if User.objects.count() > 0:
                self.load_ingredient()
                self.load_users()
                self.load_tags()
                self.load_recipes()
                self.load_recipe_tags()
                self.load_ingredient_in_recipe()
                self.load_favorites()
                self.load_shopping_carts()
                self.load_recipe_images()
            else:
                self.stdout.write(
                    self.style.ERROR(
                        'До загрузки тестовых данных необходимо создать '
                        'пользователя - администратора проекта.'
                    )
                )
        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(f'ERROR - {err}'))
            exit()
