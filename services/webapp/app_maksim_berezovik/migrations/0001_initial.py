# Generated by Django 4.2.1 on 2023-05-07 12:58

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.TextField()),
                ("name", models.TextField()),
                ("phone", models.TextField()),
            ],
        ),
    ]
