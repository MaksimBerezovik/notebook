from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from app_alexander_sidorov import api
from app_alexander_sidorov import views
from app_alexander_sidorov import viewsets

router = DefaultRouter()
router.register("addresses", viewsets.AddressViewSet)
router.register("contacts", viewsets.ContactViewSet)


urlpatterns = [
    path("api/v1/contacts/", api.ContactsView.as_view()),
    path("api/v1/contacts/<uuid:contact_id>/", api.ContactsView.as_view()),
    path("api/v2/", include(router.urls)),
    path("contacts/", views.AllContactsView.as_view()),
    path("contacts/<uuid:pk>/", views.OneContactView.as_view()),
    path("contacts/<uuid:pk>/delete/", views.DeleteContactView.as_view()),
    path("contacts/<uuid:pk>/edit/", views.UpdateContactView.as_view()),
    path("contacts/new/", views.CreateContactView.as_view()),
]
