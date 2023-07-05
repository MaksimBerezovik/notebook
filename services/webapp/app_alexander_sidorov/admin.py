from django.contrib import admin

from app_alexander_sidorov.models import Address
from app_alexander_sidorov.models import Contact
from app_alexander_sidorov.models import Tag


class AddressInline(admin.TabularInline):
    model = Address


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]


@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    ...
