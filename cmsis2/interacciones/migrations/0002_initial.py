# Generated by Django 4.2.4 on 2023-11-02 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenidos', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interacciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='contenido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='contenidos.contenido'),
        ),
        migrations.AddField(
            model_name='accion',
            name='contenido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='contenidos.contenido'),
        ),
        migrations.AddField(
            model_name='accion',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]