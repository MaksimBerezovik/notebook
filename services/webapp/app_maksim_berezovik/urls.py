from django.urls import path

from app_maksim_berezovik.contacts import contact_actions
from app_maksim_berezovik.contacts import contact_routing
from app_maksim_berezovik.views import ContactsView
from app_maksim_berezovik.views import handle_hello_view

urlpatterns = [
    path("django/contacts/<int:contact_id>/", ContactsView.as_view()),
    path("django/contacts/", ContactsView.as_view()),
    path("", handle_hello_view),
    path("contacts/", contact_routing.routing),
    path("contacts/delete/", contact_actions.delete_all_records),
    path("contacts/<int:user_id>", contact_routing.routing_edit),
]
