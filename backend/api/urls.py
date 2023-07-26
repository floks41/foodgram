"""Api application of foodgram_backend URL Configuration."""

from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserSubscriptionsViewSet,
)

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserSubscriptionsViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]
