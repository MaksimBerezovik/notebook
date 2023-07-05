from typing import Any

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField

from app_alexander_sidorov.models import Address
from app_alexander_sidorov.models import Contact


class AddressSerializer(ModelSerializer):
    contact: Any = PrimaryKeyRelatedField(
        allow_empty=False,
        many=False,
        queryset=Contact.objects.all(),
    )

    class Meta:
        fields = "__all__"
        model = Address


class ContactSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Contact


__all__ = (
    "AddressSerializer",
    "ContactSerializer",
)
