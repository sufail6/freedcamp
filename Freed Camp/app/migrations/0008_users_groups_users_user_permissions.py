# Generated by Django 4.2 on 2023-04-17 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0007_alter_users_contact_no_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='auth.group'),
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='auth.permission'),
        ),
    ]
