# Generated by Django 4.2.4 on 2023-10-01 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenidos', '0001_initial'),
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contenido',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categorias.subcategoria'),
        ),
    ]
