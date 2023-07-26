#! /bin/bash
# Выполняем миграции
python manage.py migrate
# Создаем суперпольователя
python manage.py make_admin
# Выполняем загружаем тестовые данные
python manage.py load_test_data
# Запускаем gunicorn, выход из скрипта с замещением 
exec gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi