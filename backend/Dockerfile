FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install gunicorn==20.1.0

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

RUN python manage.py collectstatic

WORKDIR /backend_static/static

WORKDIR /app

RUN cp -r /app/collected_static/. /backend_static/static/

ENTRYPOINT ["/app/docker-entrypoint.sh"]