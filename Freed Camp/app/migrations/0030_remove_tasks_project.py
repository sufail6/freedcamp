# Generated by Django 4.2 on 2023-05-03 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_add_lists_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='project',
        ),
    ]
