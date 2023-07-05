import json
from typing import Any

from framework.http import Request
from framework.http import Response
from webapp.exceptions import UnsupportedPath


# to do --- add routing in code and add new function for check Error
# check input data on TypeError, MethError and ValueError
def validate(
    request: Request,
) -> Any:
    types_dict = {"str": "", "list": [], "dict": {}}  # defaul types
    supported_types = ["str", "list", "dict"]

    url_list = request.path.split("/")
    if url_list[4] not in supported_types:
        raise TypeError("TypeError: unsupported type")
    if hasattr(types_dict[url_list[4]], url_list[5]) == 0:
        raise TypeError(
            f"TypeError: unknown method {url_list[4]}.{url_list[5]}"
        )
    data = json.loads(request.params["value"][0])
    if isinstance(data, type(types_dict[url_list[4]])) == 0:
        raise TypeError(f"ValueError: {data} is not {url_list[4]}")


# if path /~/maksim_berezovik
def handle_hello_from(
    requests: Request,
) -> Any:
    if namelist := requests.params.get("name"):  # noqa: S113
        name = namelist[0]
        result = f"Hello {name} from Maksim Berezovik"
        return Response(body=result.encode())
    return Response(body="Hello from Maksim Berezovik".encode())


# if path /~/maksim_berezovik/meth/<type>/<meth>?value=<data>
def handle_meth(request: Request) -> Any:  # noqa: CCR001
    url_list = request.path.split("/")  # get list with meth and type
    validate(request)
    if request.params.get("value") and request.params.get("q"):
        if first_arg_code := request.params.get("value"):
            first_arg: str = json.loads(first_arg_code[0])
        if second_arg_code := request.params.get("q"):
            second_arg: str = json.loads(second_arg_code[0])
        if url_list[4].lower() == "list":
            getattr(first_arg, url_list[5])(second_arg)
            result = first_arg
        else:
            result = getattr(first_arg, url_list[5])(second_arg)
        return Response(body=(json.dumps(result)).encode())

    if datalist := request.params.get("value"):
        data = json.loads(datalist[0])
        if url_list[4].lower() == "list":
            getattr(data, url_list[5])()
            result = data
        else:
            result = getattr(data, url_list[5])()
        try:
            resp = Response(body=(json.dumps(result)).encode())
            return resp
        except TypeError:
            return Response(body=(json.dumps(str(result))).encode())


# dict[str, Callable[[dict], str | None]]
routs: Any = {  # dict for routing
    "/~/maksim_berezovik/meth": handle_meth,
    "/~/maksim_berezovik": handle_hello_from,
}


def main(request: Request) -> Any:  # main function
    path: str = request.path
    # params: dict = request.params
    for route, hand in routs.items():
        if path.startswith(route):
            handler = hand
            break
    else:
        raise UnsupportedPath
    try:
        return handler(request)
    except TypeError as e:
        return Response(body=(json.dumps(str(e))).encode())
