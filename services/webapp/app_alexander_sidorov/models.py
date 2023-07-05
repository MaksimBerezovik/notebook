from typing import Any
from uuid import uuid4

from django.db import models

from framework.debugging import performance_meter_2000
from framework.debugging import performance_meter_9000


class ContactManager(models.Manager):
    pass


class Contact(models.Model):
    objects = ContactManager()

    id: Any = models.UUIDField(  # noqa:A003,VNE003
        default=uuid4,
        primary_key=True,
        verbose_name="ID",
    )
    name: Any = models.TextField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Полное имя",
    )
    phone: Any = models.TextField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="Телефон",
    )

    @performance_meter_2000
    def get_absolute_url(self) -> str:
        with performance_meter_9000("get contact pk"):
            pk = self.pk
        with performance_meter_9000("form an url using f-string"):
            msg = f"/alexander_sidorov/contacts/{pk}/"
        with performance_meter_9000("return url"):
            return msg


class AddressManager(models.Manager):
    pass


class Address(models.Model):
    objects = AddressManager()

    city = models.TextField()
    street = models.TextField()

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class TagManager(models.Manager):
    pass


class Tag(models.Model):
    objects = TagManager()

    label = models.TextField(unique=True)

    contacts = models.ManyToManyField(Contact)
