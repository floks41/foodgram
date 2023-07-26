"""Настройки административной панели для моделей приложения Users."""

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройки отображения модели User в административной панели."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'username',
    )
    search_fields = (
        'username__icontains',
        'email__icontains',
    )
