# Generated by Django 4.2.4 on 2023-11-02 21:45

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cuerpo', django_quill.fields.QuillField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_caducidad', models.DateField(blank=True, null=True)),
                ('fecha_publicacion', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('BORRADOR', 'Borrador'), ('EDICION', 'En Edición'), ('REVISION', 'En Revision'), ('PUBLICADO', 'Publicado'), ('RECHAZADO', 'Rechazado'), ('INACTIVO', 'Inactivo')], max_length=100)),
                ('cantidad_denuncias', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad_me_gusta', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad_compartir', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad_comentarios', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad_visualizaciones', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plantilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField()),
                ('plantilla', django_quill.fields.QuillField()),
            ],
        ),
    ]
