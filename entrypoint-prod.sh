#!/bin/sh

sleep 5

python manage.py migrate --no-input
python manage.py collectstatic --noinput

gunicorn cmsis2.wsgi:application --bind 0.0.0.0:8000