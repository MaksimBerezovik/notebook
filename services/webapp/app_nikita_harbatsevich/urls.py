from django.urls import path

from app_nikita_harbatsevich import views

urlpatterns = [
    path("", views.handle_hello_world),
]
