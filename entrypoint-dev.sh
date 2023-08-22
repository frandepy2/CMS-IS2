#!/bin/sh

sleep 5
echo "Inicia el proceso de hacer migraciones"
python manage.py makemigrations usuarios
echo "finaliza el proceso de hacer migraciones"
python manage.py migrate --no-input
python manage.py collectstatic --noinput


python manage.py runserver 0.0.0.0:8000