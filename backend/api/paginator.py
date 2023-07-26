"""Модуль настройки паджинации для приложения Api."""

from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Настройки паджинации."""

    page_size = 8
    max_page_size = 25
    page_size_query_param = 'limit'
