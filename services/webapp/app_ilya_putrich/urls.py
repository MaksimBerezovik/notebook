from django.urls import path

from app_ilya_putrich import views

urlpatterns = [
    path("", views.handle_hello_world),
]
