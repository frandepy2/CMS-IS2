# your_app_name/cron.py
from django.utils import timezone
from .models import Contenido


def my_first_cron():
    print("THE CRON WORKS VERY WELL")

    current_date = timezone.now().date()
    outdated_content = Contenido.objects.filter(
        fecha_caducidad__lt=current_date
    )
    print(current_date)
    for content in outdated_content:
        print(content.fecha_caducidad)
        content.estado = 'INACTIVO'
        content.save()

