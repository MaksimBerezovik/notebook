from django.db import models


class Contacts(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
