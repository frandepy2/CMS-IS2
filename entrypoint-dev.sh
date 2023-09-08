#!/bin/sh

sleep 5
echo "Inicia el proceso de hacer migraciones"
python manage.py makemigrations usuarios roles categorias
echo "finaliza el proceso de hacer migraciones"
python manage.py migrate --no-input
echo "Inicia el proceso de guardar la base de datos"
python manage.py shell < load_database.py
echo "finaliza el proceso de guardar la base de datos"
python manage.py collectstatic --noinput


python manage.py runserver 0.0.0.0:8000