# Generated by Django 4.2.4 on 2023-11-30 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0002_notificacion_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
