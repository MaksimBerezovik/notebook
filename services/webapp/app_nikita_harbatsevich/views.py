from django.http import HttpRequest
from django.http import HttpResponse

from framework.debugging import debug


def handle_hello_world(request: HttpRequest) -> HttpResponse:
    debug(request)
    return HttpResponse("hello from Nikita Harbatsevich")
