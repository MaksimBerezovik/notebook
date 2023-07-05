from rest_framework.viewsets import ModelViewSet

from app_alexander_sidorov.models import Address
from app_alexander_sidorov.models import Contact
from app_alexander_sidorov.serializers import AddressSerializer
from app_alexander_sidorov.serializers import ContactSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


__all__ = (
    "AddressViewSet",
    "ContactViewSet",
)
