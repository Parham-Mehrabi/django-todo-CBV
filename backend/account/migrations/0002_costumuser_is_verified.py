# Generated by Django 4.2 on 2023-04-29 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="costumuser",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
