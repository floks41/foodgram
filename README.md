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
> IP: 158.160.66.88

> Сайт: https://choa.zapto.org/

> Панель администратора: https://choa.zapto.org/admin/

### Администратор:
> login: admin@fake.up

> password: admin728

[![Сайт Foodgram Рецепты](screen_shot.jpg)]

### Структура проекта
- frontend - файлы фронтенда приложения на React, запускаются только для сборки;
- infra — инфраструктура проекта: конфигурационный файл nginx, docker-compose.yml и docker-compose.production.yml;
- backend - файлы бекенда приложения - это и есть курсовой проект;
- backend/data - содержит файлы в формате csv с тестовыми данными для проверки работы проекта, а также текстовые изображения к рецептам.
### Тестовые данные
 - для создания тестового суперпользователя-администратора необходимо выполнить команду `python3 manage.py make_admin` (будет созда пользователь с username: admin и паролем из файла .env)
 - для загрузки тестовых данных - команду `python3 manage.py load_test_data`

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

# Как запустить проект

## Локальный запуск проекта (backend запускается локально, остальные части в контейнерах docker compose)
1. Скопируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:chuzhmarov/foodgram.git (https://github.com/chuzhmarov/foodgram.git)
```

```
cd foodgram
```

2. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

3. Установите зависимости из файла requirements.txt:

```
cd backend
```

```
python3 -m pip install --upgrade pip
```
pip install -r requirements.txt
```
```
4. В корневой папке проекта находится файл .env.example cоздайте по аналогии с ним фаил .env: 

```
POSTGRES_DB=kotogram
POSTGRES_USER=kotogram_user
POSTGRES_PASSWORD=kotogram_password
DB_HOST=database_host
DB_PORT=5432 
SECRET_KEY=django-settings-secret-key
ALLOWED_HOSTS=127.0.0.1 localhost backend
ADMIN_PASSWORD=super_secret_password_for_username_admin
```
5. Примените следующие настройки docker compose например из файла 'docker-compose.local.yml':

```
version: '3.3'
volumes:
  static:
  media:
  pg_data:
services:
  db:
    image: postgres:13
    env_file:
      - .env
    ports:
      - 5432:5432
    volumes:
      - pg_data:/var/lib/postgresql/data/
    healthcheck:
      test: [ "CMD", "pg_isready", "-q", "-d", "${POSTGRES_DB}", "-U", "${POSTGRES_USER}" ]
      timeout: 45s
      interval: 10s
      retries: 10
    
  frontend:
    build: ./frontend
    env_file: .env
    command: cp -r /app/build/. /static/
    volumes:
      - static:/static

  gateway:
    build: ./nginx/
    env_file: .env
    ports:
      - "80:80"
    volumes:
      - static:/static
      - media:/media
      - ./docs/:/usr/share/nginx/html/api/docs/
```  
6. Примените следующие настройки для 'nginx.conf':

```
server {
    listen 80;
    location /api/ {
        proxy_pass http://host.docker.internal:8000;
    }
    location /admin/ {
        proxy_pass http://host.docker.internal:8000/admin/;
    }
    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.html;
    }
    location / {
        alias /static/;
        try_files $uri $uri/ /index.html;
    }
     
}
```
7. Перейдите в корень проекта 'foodgram' и выполните команду сборки контейнеров:
```
cd ..
```
```
sudo docker compose -f docker-compose.local.yml up
```
Документация по API в формате ReDOC по адресу `http://localhost/api/docs/redoc.html`

8. Выполните миграции:

```
cd backend
```
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
9. Соберите статику бекэнда и посместите в volume `static` для контейнера `gateway`.

```
python3 manage.py collectstatic
```
  Найдите контейнер `gateway` при помощи команды `sudo docker container ls` и скопируйте статику бекенда

```
sudo docker cp collected_static/. <gateway_container_id>:/static
```

10. Для создания тестового суперпользователя (администратора) и загрузки тестовых данных выполните команды:

```
python3 manage.py make_admin
```
```
python3 manage.py load_test_data
```
11. Запустите бекэнд сервер:

```
python3 manage.py runserver
```
Приложение будет доступно на локальной машине по адресу http://localhost/

## Запуск проекта в контейнерах docker compose (образы на Dockerhub) локально или на сервере

1. Создайте и перейдите в директорию, например, `Foodgram`

```
mkdir foodgram
```
```
cd foodgram
```
2. Поместите в указанную директорию файлы `.env` и `docker-compose.production.yml`

3. Запустите контейнеры

```
sudo docker compose -f docker-compose.production.yml up --build -d
```
4. Приложение будет доступно локально по адресу `http://localhost:9000/`.

   При запуске контейнера backend автоматически будет создан суперпользователь с правами администратора username: admin, с паролем, указанным в .env., выполненфы миграции и созданы несколько тестовых пользователей, загружены тестовые данные, включая ингредиенты, теги, рецепты, изображениями рецептов, подписки, избранное, корзины для покупок.

5. Примените на сервере настройки внешнего nginx, например такие:

```
server {
    
    server_name 158.160.66.88 choa.zapto.org;
    server_tokens off;
    location / {
        proxy_set_header Host $http_host;
	proxy_pass http://127.0.0.1:9000;
    }

} 
```
6. Приложение будет доступно локально по адресу `http://choa.zapto.org/`




