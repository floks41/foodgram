![Документация Foodgram](povar.jpg)

# Курсовой проект Foodgram
## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![Djoser](https://img.shields.io/badge/-Djoser-464646?style=flat-square&logo=Djoser)](https://djoser.readthedocs.io/en/latest/getting_started.html)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
### Разработчик:

👨🏼‍💻Олег: https://github.com/chuzhmarov

:small_orange_diamond: **Пояснение.**
> Проект Foodgram «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
Задачей курсового проекта является разработка бекенда приложения Foodgr

## Проект развернут для проверки 
### Адрес проект:
> IP: 158.160.66.88;\
> Сайт: https://choa.zapto.org/;\
> Панель администратора: https://choa.zapto.org/admin/;\
### Администратор:
> login: admin@fake.up;\
> password: admin728;

[![Сайт Foodgram Рецепты](screen_shot.jpg)]

### Структура проекта
- frontend - файлы фронтенда приложения на React, запускаются только для сборки;
- infra — инфраструктура проекта: конфигурационный файл nginx, docker-compose.yml и docker-compose.production.yml;
- backend - файлы бекенда приложения - это и есть курсовой проект;
- backend/data - содержит файлы в формате csv с тестовыми данными для проверки работы проекта, а также текстовые изображения к рецептам.
### Тестовые данные
 - для создания тестового суперпользователя-администратора необходимо выполнить команду `python manage.py make_admin` (будет созда пользователь с username: admin и паролем из файла .env)
 - для загрузки тестовых данных - команду `python manage.py load_test_data`

### Технологии
- Python 3.9
- Django 3.2.19
- Django Rest Framework 3.14.0
- Djoser 2.2.0
- PostgreSQL 13
- Nginx 1.22.1
- Docker Compose 3.3

### Описание проекта
Что могут делать неавторизованные пользователи:
- Создать аккаунт;
- Просматривать рецепты на главной;
- Просматривать отдельные страницы рецептов;
- Фильтровать рецепты по тегам;

Что могут делать авторизованные пользователи:
- Входить в систему под своим логином и паролем;
- Выходить из системы (разлогиниваться);
- Менять свой пароль;
- Создавать/редактировать/удалять собственные рецепты;
- Просматривать рецепты на главной;
- Просматривать страницы пользователей;
- Просматривать отдельные страницы рецептов;
- Фильтровать рецепты по тегам;
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов;
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок;
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок;

Что могут делать администраторы:
- Администратор обладает всеми правами авторизованного пользователя;
- (панель администратора) Изменять пароль любого пользователя;
- (панель администратора) создавать/блокировать/удалять аккаунты пользователей;
- (панель администратора) редактировать/удалять любые рецепты;
- (панель администратора) добавлять/удалять/редактировать ингредиенты;
- (панель администратора) добавлять/удалять/редактировать теги;

### Документация
Подробное описание ресурсов доступно в документации после запуска проекта по адресу `http://localhost/api/docs/`.

В документации указаны ресурсы, разрешённые типы запросов, права доступа и дополнительные параметры (паджинация, поиск, фильтрация и т.д.), там где это необходимо.