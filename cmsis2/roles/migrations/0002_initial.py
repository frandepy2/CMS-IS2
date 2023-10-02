# Generated by Django 4.2.4 on 2023-09-30 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usercategoryrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roles.custompermission'),
        ),
        migrations.AddField(
            model_name='rolepermission',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roles.customrole'),
        ),
        migrations.AddField(
            model_name='customrole',
            name='permissions',
            field=models.ManyToManyField(through='roles.RolePermission', to='roles.custompermission'),
        ),
        migrations.AlterUniqueTogether(
            name='usercategoryrole',
            unique_together={('user', 'category', 'role')},
        ),
    ]
