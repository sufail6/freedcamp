# Generated by Django 4.2 on 2023-04-17 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0008_users_groups_users_user_permissions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='UserProfile',
        ),
    ]
