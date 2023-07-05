# Create your models here.
from django.db import models


class Contact(models.Model):
    user_id = models.IntegerField(verbose_name="Id контакта")
    name = models.TextField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Имя контакта",
        help_text="Введите контакт в формате <Имя> <Фамиля>",
    )
    phone = models.TextField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Номер контакта",
        help_text="Вводите номер в формате <код страны>"
        "<код опреатора><номертелефона>",
    )
