# Generated by Django 4.2 on 2023-04-26 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_add_lists_project_remove_tasks_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='project',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='app.projects'),
        ),
    ]
