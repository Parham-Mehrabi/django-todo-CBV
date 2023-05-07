# Generated by Django 4.2 on 2023-04-11 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("todo", "0002_rename_task_task_context_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="author",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="context",
            field=models.TextField(blank=True),
        ),
    ]
