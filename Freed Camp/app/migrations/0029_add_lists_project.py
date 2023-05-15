# Generated by Django 4.2 on 2023-05-03 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_remove_add_lists_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_lists',
            name='project',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='add_list', to='app.projects'),
        ),
    ]
