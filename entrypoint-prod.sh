#!/bin/sh

sleep 5
echo "Inicia el proceso de hacer migraciones"
python manage.py makemigrations usuarios roles categorias
echo "finaliza el proceso de hacer migraciones"
python manage.py migrate --no-input
python manage.py collectstatic --noinput

gunicorn cmsis2.wsgi:application --bind 0.0.0.0:8000