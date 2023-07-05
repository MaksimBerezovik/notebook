from django.contrib import admin
from django.urls import include
from django.urls import path

import project.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("alexander_sidorov/", include("app_alexander_sidorov.urls")),
    path("dmitriy_zhdanovich/", include("app_dmitriy_zhdanovich.urls")),
    path("drf/", include("rest_framework.urls")),
    path("egor_pyshny/", include("app_egor_pyshny.urls")),
    path("ilya_putrich/", include("app_ilya_putrich.urls")),
    path("livez/", project.views.handle_livez),
    path("maksim_berezovik/", include("app_maksim_berezovik.urls")),
    path("nikita_harbatsevich/", include("app_nikita_harbatsevich.urls")),
    path("vadim_zhurau/", include("app_vadim_zhurau.urls")),
]
