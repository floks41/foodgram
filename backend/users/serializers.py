"""Модуль сериализаторов приложения Users."""

from djoser.serializers import (
    UserCreateSerializer as DjoserStandartUserCreateSerializer,
)
from djoser.serializers import UserSerializer as DjoserStandartUserSerializer
from rest_framework import serializers

from recipes.models import Subscription
from users.models import User


class DjoserUserCreateSerializer(DjoserStandartUserCreateSerializer):
    """Сериализатор для создания пользователя.

    Подключается к приложению djoser в настройках django-проекта."""

    class Meta(DjoserStandartUserCreateSerializer.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
        )
        read_only_fields = ('id',)


class DjoserUserSerializer(DjoserStandartUserSerializer):
    """Сериализатор для пользователя.

    Подключается к приложению djoser в настройках django-проекта."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserStandartUserSerializer.Meta):
        fields = DjoserStandartUserSerializer.Meta.fields + ('is_subscribed',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, obj):
        user: User = self.context.get('request').user
        return (
            user.is_authenticated
            and Subscription.objects.filter(user=user, author=obj).exists()
        )
