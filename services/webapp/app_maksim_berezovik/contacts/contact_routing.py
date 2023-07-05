from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_maksim_berezovik.contacts.contact_actions import handel_create_contact
from app_maksim_berezovik.contacts.contact_actions import handel_delete_contact
from app_maksim_berezovik.contacts.contact_actions import handel_update_contact
from app_maksim_berezovik.contacts.contact_actions import handel_view_contact
from app_maksim_berezovik.contacts.contact_actions import handel_view_contacts


@csrf_exempt
def routing(request: HttpRequest) -> HttpResponse:
    method = request.method
    if method == "GET":
        return HttpResponse(handel_view_contacts())
    if method == "POST":
        return HttpResponse(handel_create_contact(request))
    return HttpResponse(status=405)


@csrf_exempt
def routing_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    method = request.method
    if method == "GET":
        return handel_view_contact(request, user_id)
    if method == "PATCH":
        return handel_update_contact(request, user_id)
    if method == "DELETE":
        return handel_delete_contact(request, user_id)
    return HttpResponse(status=405)
