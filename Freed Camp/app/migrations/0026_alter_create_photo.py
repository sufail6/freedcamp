# Generated by Django 4.2 on 2023-05-02 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_create_photo_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create',
            name='photo',
            field=models.ImageField(blank=True, default='assets/img/default.jpg', null=True, upload_to='profile/'),
        ),
    ]
