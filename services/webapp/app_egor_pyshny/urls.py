from django.urls import path

from app_egor_pyshny import views

urlpatterns = [
    path("", views.hello_msg),
    path(
        "lesson05/<type_>/<meth>/",
        views.types_operations,
    ),
]
