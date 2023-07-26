"""Модуль функций обработки исключений для приложения Api."""

from rest_framework.views import exception_handler


def non_field_errors_exception_handler(exc, context):
    """Обработчик исключений.

    Изменяет предстапвление данных об ошибках при non_field_error.
    """

    response = exception_handler(exc, context)

    if response is not None and 'non_field_errors' in response.data:
        custom_data = {}
        custom_data['errors'] = str(*response.data.get('non_field_errors'))

        response.data = custom_data

    return response
