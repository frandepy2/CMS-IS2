# Generated by Django 4.2.4 on 2023-10-14 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interacciones', '0002_accion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accion',
            unique_together=set(),
        ),
    ]