import json

from django.http import HttpRequest
from django.http import HttpResponse


def hello_msg(request: HttpRequest) -> HttpResponse:
    res = "Hello from Egor Pyshny"
    if name := request.GET.get("name"):
        name = name.strip().replace('"', "")
        if name != "":
            res = f"Hello {name} from Egor Pyshny"
    return HttpResponse(res)


def validate(curtype: str, meth: str, obj: object) -> None:
    if obj is None:
        raise RuntimeError("no value")
    _types = ["list", "dict", "str"]
    if curtype not in _types:
        raise RuntimeError("TypeError: unsupported type")
    objtype = str(type(obj))
    objtype = objtype.split(" ")[1].replace(">", "").replace("'", "")
    if not objtype == curtype:
        raise RuntimeError(f"ValueError: {str(obj)} is not {curtype}")
    if not hasattr(obj, meth):
        raise RuntimeError(f"TypeError: unknown method {curtype}.{meth}")
    return None


def types_operations(  # noqa: CCR001
    request: HttpRequest, type_: str, meth: str
) -> HttpResponse:  # noqa: CCR001
    argv = []
    if arg_list := request.GET.get("argv"):
        arg_string = arg_list.replace("'", '"')
        argv = json.loads(arg_string)
    obj: object = None
    if obj_list := request.GET.get("value"):
        obj_string: str = obj_list.replace("'", '"')
        obj = json.loads(obj_string)
    validate(type_, meth, obj)
    argv_copy = argv
    while True:
        try:
            res: str | None = getattr(obj, meth)(*argv_copy)
            if res is not None:
                return HttpResponse(res)
            else:
                return HttpResponse(json.dumps(obj))
        except Exception as e:
            if ("is not in" in str(e)) or ("substring not" in str(e)):
                raise RuntimeError("no such value")
            if len(argv_copy) == 0:
                raise RuntimeError("wrong arguments")
        argv_copy = argv[: len(argv_copy) - 1]
    return HttpResponse()


# Create your views here.
