from django.urls import path

from app_vadim_zhurau import views

urlpatterns = [
    path("", views.handle_hello_world),
]
