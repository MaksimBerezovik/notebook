# Generated by Django 4.2.1 on 2023-05-12 16:22

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        (
            "app_maksim_berezovik",
            "0002_alter_contact_name_alter_contact_phone_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="user_id",
            field=models.IntegerField(verbose_name="Id контакта"),
        ),
    ]
