# Generated by Django 4.2 on 2023-04-13 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_delete_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='contact_no',
            field=models.IntegerField(default=0),
        ),
    ]