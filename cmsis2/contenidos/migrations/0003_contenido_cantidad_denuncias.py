# Generated by Django 4.2.4 on 2023-10-01 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenidos', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='cantidad_denuncias',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]