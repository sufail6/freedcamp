# Generated by Django 4.2 on 2023-04-15 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_is_customer_login_is_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='contact_no',
            field=models.CharField(max_length=30),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
