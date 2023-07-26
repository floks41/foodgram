"""Модуль административной команды создания суперпользователя."""

import os

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from users.models import User

ADMIN = {
    'username': 'admin',
    'email': 'admin@fake.up',
    'last_name': 'Pushkin',
    'first_name': "Aleksander",
    'is_staff': True,
    'is_superuser': True,
}
PASSWORD = os.getenv('ADMIN_PASSWORD', None)


class Command(BaseCommand):
    """Административная команда для создания суперпользователя
    с предустановленными параметрами.
    """

    help = 'Создает суперпользователя с предустановленными параметрами.'

    def make_admin(self):
        """Создать админа."""

        user, created = User.objects.get_or_create(**ADMIN)

        if user and created and PASSWORD:
            user.set_password(PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан.'))
        else:
            self.stdout.write(
                self.style.ERROR(
                    'При создании суперпользователя возникли ошибки. '
                    'Пароль не установлен.'
                )
            )

    def handle(self, *args, **options):
        """Исполнение административной команды."""

        try:
            self.make_admin()
        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(f'ERROR - {err}'))
            exit()
        exit(0)
