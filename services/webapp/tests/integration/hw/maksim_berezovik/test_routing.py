import json
from urllib.parse import urlencode

import httpx
import pytest

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
]


async def test_routing_happy(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovik")
    assert resp.status_code == 200
    assert "Hello from Maksim Berezovik" in resp.text


async def test_routing_happy_two(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovik/")
    assert resp.status_code == 200
    assert "Hello from Maksim Berezovik" in resp.text


async def test_routing_fail_path(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovi")
    assert resp.status_code == 404
    assert "Hello from Maksim Berezovik" not in resp.text


async def test_routing_happy_query_2(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get(
        "/~/maksim_berezovik?name=Vika"
    )
    assert resp.status_code == 200
    assert "Hello Vika from Maksim Berezovik" in resp.text


async def test_routing_fail_query_1(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovik/?nnnn")
    assert resp.status_code == 200
    assert "Hello from Maksim Berezovik" in resp.text


async def test_routing_fail_query_2(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovik?nnnn")
    assert resp.status_code == 200
    assert "Hello from Maksim Berezovik" in resp.text


async def test_routing_happy_query_str_1(
    web_client: httpx.AsyncClient,
) -> None:
    resp: httpx.Response = await web_client.get(
        "/~/maksim_berezovik/meth/str/title?value=%22heLLO+worLD%22"
    )
    assert resp.status_code == 200
    assert "Hello World" in json.loads(resp.text)


async def test_routing_happy_query_str_2(
    web_client: httpx.AsyncClient,
) -> None:
    resp: httpx.Response = await web_client.get(
        "/~/maksim_berezovik/meth/str/upper?value=%22heLLO+worLD%22"
    )
    assert resp.status_code == 200
    assert "HELLO WORLD" in json.loads(resp.text)


async def test_routing_happy_query_list(
    web_client: httpx.AsyncClient,
) -> None:
    data: list = [4, 3, 2, 1]
    parametrs = json.dumps(data)
    query_str = urlencode({"value": parametrs})
    # + str(urlencode({"value": json.dumps([4, 3, 2, 1])}))
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/list/sort?{query_str}"
    )
    assert resp.status_code == 200
    assert [1, 2, 3, 4] == json.loads(resp.text)


async def test_routing_happy_query_dict(
    web_client: httpx.AsyncClient,
) -> None:
    data: dict = {"number": "[1, ,2, 3, 4]"}
    parametrs = json.dumps(data)
    query_str = urlencode({"value": parametrs})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/dict/keys?{query_str}"
        # str(urlencode({"value": json.dumps({"number": "[1, ,2 3, 4]"})}))
    )
    assert resp.status_code == 200
    assert json.loads(resp.text) == "dict_keys(['number'])"


async def test_routing_fail_type(web_client: httpx.AsyncClient) -> None:
    data: dict = {"number": [4, 3, 2, 1]}
    parametrs = json.dumps(data)
    query_str = urlencode({"value": parametrs})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/dit/keys?{query_str}"
        # str(urlencode({"value": json.dumps({"number": [4, 3, 2, 1]})}))
    )
    assert resp.status_code == 200
    assert "TypeError: unsupported type" in resp.text


async def test_routing_fail_method(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get(
        "/~/maksim_berezovik/meth/str/ttle?value=heLLo+worlD"
    )
    assert resp.status_code == 200
    assert "TypeError: unknown method str.ttle" in resp.text


async def test_routing_fail_value(web_client: httpx.AsyncClient) -> None:
    data: list = [4, 3, 2, 1]
    parametrs = json.dumps(data)
    query_str = urlencode({"value": parametrs})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/str/title?{query_str}"
        # str(urlencode({"value": json.dumps([4, 3, 2, 1])}))
    )
    assert resp.status_code == 200
    assert "ValueError: [4, 3, 2, 1] is not str" in resp.text


async def test_routing_happy_query_2_parametrs_str(
    web_client: httpx.AsyncClient,
) -> None:
    data: str = "number"
    data2: str = "num"
    parametrs = json.dumps(data)
    parametrs2 = json.dumps(data2)
    query_str = urlencode({"value": parametrs, "q": parametrs2})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/str/startswith?{query_str}"
        # str(urlencode({"value": json.dumps("number"), "q": "num"}))
    )
    assert resp.status_code == 200
    assert json.loads(resp.text)


async def test_routing_happy_query_2_parametrs_list(
    web_client: httpx.AsyncClient,
) -> None:
    data: list = []
    data2: str = "num"
    parametrs = json.dumps(data)
    parametrs2 = json.dumps(data2)
    query_str = urlencode({"value": parametrs, "q": parametrs2})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/list/append?{query_str}"
        # str(urlencode({"value": json.dumps([]), "q": "num"}))
    )
    assert resp.status_code == 200
    assert ["num"] == json.loads(resp.text)


async def test_routing_happy_query_2_parametrs_dict(
    web_client: httpx.AsyncClient,
) -> None:
    data: dict = {"num": ["xxx"]}
    data2: str = "num"
    parametrs = json.dumps(data)
    parametrs2 = json.dumps(data2)
    query_str = urlencode({"value": parametrs, "q": parametrs2})
    resp: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/meth/dict/get?{query_str}"
        # str(urlencode({"value": json.dumps({"num": ["xxx"]}), "q": "num"}))
    )
    assert resp.status_code == 200
    assert ["xxx"] == json.loads(resp.text)


@pytest.mark.xfail
@pytest.mark.parametrize(
    "path,status,result",
    [["/~/maksim_berezovik/contacts", 200, {"items": []}]],
)
async def test_contacts_view(
    web_client: httpx.AsyncClient, path: str, status: int, result: dict
) -> None:
    resp: httpx.Response = await web_client.get(path)
    assert resp.status_code == status
    assert json.loads(resp.text) == result


# @pytest.mark.xfail
@pytest.mark.parametrize(
    "path,data_c,status,result",
    [
        [
            "/~/maksim_berezovik/contacts",
            {"name": "Maksim Berezovik", "phone": "+375259641650"},
            201,
            {"name": "Maksim Berezovik", "phone": "+375259641650"},
        ],
        [
            "/~/maksim_berezovik/contacts",
            {"name": "Igor Igorev", "phone": "+375295555555"},
            201,
            {"name": "Maksim Berezovik", "phone": "+375259641650"},
        ],
        [
            "/~/maksim_berezovik/contacts",
            {"name": "No name", "phone": "+375297777777"},
            201,
            {"name": "No name", "phone": "+375297777777"},
        ],
    ],
)
async def test_contact_add(
    web_client: httpx.AsyncClient,
    path: str,
    data_c: dict,
    status: int,
    result: dict,
) -> None:
    resp: httpx.Response = await web_client.post(path, json=data_c)
    assert resp.status_code == 201


async def test_contact_id(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/~/maksim_berezovik/contacts")
    contact_id = json.loads(resp.text)["items"][2]["user_id"]
    result: dict = {
        "user_id": contact_id,
        "name": "No name",
        "phone": "+375297777777",
    }
    resp_id: httpx.Response = await web_client.get(
        f"/~/maksim_berezovik/contacts/{contact_id}"
    )
    assert resp_id.status_code == 200
    assert json.loads(resp_id.text) == result


async def test_patch_contact(web_client: httpx.AsyncClient) -> None:
    path = "/~/maksim_berezovik/contacts"
    resp: httpx.Response = await web_client.get(path)
    contact_id = json.loads(resp.text)["items"][2]["user_id"]
    body = {"phone": "No phone"}
    resp_patch: httpx.Response = await web_client.patch(
        f"{path}/{contact_id}", json=body
    )
    result = {"user_id": contact_id, "name": "No name", "phone": "No phone"}
    assert resp_patch.status_code == 200
    assert json.loads(resp_patch.text) == result


async def test_del_contact(web_client: httpx.AsyncClient) -> None:
    path = "/~/maksim_berezovik/contacts"
    resp: httpx.Response = await web_client.get(path)
    contact_id = json.loads(resp.text)["items"][2]["user_id"]
    resp_del: httpx.Response = await web_client.delete(f"{path}/{contact_id}")
    assert resp_del.status_code == 204


async def test_del_all_records(web_client: httpx.AsyncClient) -> None:
    path = "/~/maksim_berezovik/contacts/delete"
    resp: httpx.Response = await web_client.get(path)
    assert resp.status_code == 200
    assert json.loads(resp.text) == "База очищена"


async def test_routing_happy_django_1(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/maksim_berezovik/")
    assert resp.status_code == 200
    assert "Hello from Maksim Berezovik" in resp.text


async def test_routing_happy_django_2(web_client: httpx.AsyncClient) -> None:
    resp: httpx.Response = await web_client.get("/maksim_berezovik/?name=GGG")
    assert resp.status_code == 200
    assert "Hello GGG from Maksim Berezovik" in resp.text
