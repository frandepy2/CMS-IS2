#!/bin/sh

sleep 10
echo "Inicia el proceso de hacer migraciones"
python manage.py makemigrations usuarios roles categorias contenidos parametros interacciones reportes notificaciones
echo "finaliza el proceso de hacer migraciones"
python manage.py migrate --no-input

python manage.py collectstatic --noinput

echo "activa los crontab"
python manage.py crontab add

# Check if the /etc/inittab file exists
if [ -f /etc/inittab ]; then
    # Add the cron service to the sysinit process in /etc/inittab
    echo "::sysinit:/etc/init.d/cron start" | tee -a /etc/inittab > /dev/null

    # Inform the user about the change
    echo "Added cron service to /etc/inittab for automatic startup."
else
    echo "Error: /etc/inittab file not found. Please check your system configuration."
fi

#activa el servicio cron
crond -b

gunicorn cmsis2.wsgi:application --bind 0.0.0.0:8000