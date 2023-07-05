from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app_dmitriy_zhdanovich import views
from app_dmitriy_zhdanovich.views import CrudContacts

view_app = csrf_exempt(CrudContacts.as_view())

urlpatterns = [
    path("", views.handle_hello_world),
    path(
        "lesson05/<type_>/<meth>/",
        views.python_data_structures_methods,  # type: ignore
    ),
    path("contacts/", view_app),
    path("contacts/<int:contact_id>", view_app),
]
