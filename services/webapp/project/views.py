from django.http import HttpRequest
from django.http import HttpResponse


def handle_livez(request: HttpRequest) -> HttpResponse:
    assert request
    return HttpResponse("alive")
