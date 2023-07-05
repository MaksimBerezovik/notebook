from typing import cast
from uuid import uuid4

from django import forms
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app_alexander_sidorov.models import Contact


class AllContactsView(ListView):
    model = Contact


class ContactForm(forms.ModelForm):
    class Meta:
        fields = ("name", "phone")
        model = Contact
        widgets = {
            "name": forms.TextInput(attrs={"min-width": "100px"}),
            "phone": forms.TextInput(attrs={"min-width": "100px"}),
        }

    def save(self, commit: bool = True) -> Contact:
        obj = super().save(commit=False)
        if not obj.id:
            obj.id = uuid4()
        obj = super().save(commit=commit)
        return cast(Contact, obj)


class CreateContactView(CreateView):
    extra_context = {"page_header": "Создать контакт"}
    form_class = ContactForm
    model = Contact
    success_url = "/alexander_sidorov/contacts/"


class OneContactView(DetailView):
    model = Contact


class UpdateContactView(UpdateView):
    extra_context = {"page_header": "Обновить контакт"}
    form_class = ContactForm
    model = Contact


class DeleteContactView(DeleteView):
    model = Contact
    success_url = "/alexander_sidorov/contacts/"
