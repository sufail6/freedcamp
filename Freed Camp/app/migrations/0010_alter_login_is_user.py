# Generated by Django 4.2 on 2023-04-17 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_users_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='is_user',
            field=models.BooleanField(default=True),
        ),
    ]
