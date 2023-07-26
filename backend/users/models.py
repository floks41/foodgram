"""Модуль моделей приложения Users."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text=_(
            'Обязательное. Не более 150 символов. ' 'Буквы, цифры и только @/./+/-/_.'
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text=_('Обязательное. Не более 150 символов.'),
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text=_('Обязательное. Не более 150 символов.'),
        blank=True,
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254,
        help_text=_('Обязательное. Не более 254 символов.'),
        error_messages={
            'unique': _('Пользователь с указанным email уже существует.'),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password', 'id')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='Unique_email_for_each_username',
            )
        ]
        ordering = ('id',)
