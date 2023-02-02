from fastapi.testclient import TestClient
from fastapi import status
from main import app

from pydantic.tools import parse_obj_as
from schema import user,generic
import json
import httpx

router = TestClient(app=app)

def test_user_register():
    user_json:user.UserSchema = user.UserSchema(
            id=0,
            user_name="prueba",
            email="prueba@gmail.com",
            name= "prueba",
            last_name= "prueba",
            password= "prueba123"
            )
    response = router.post("/users/register",json=user_json.dict())
    #response = httpx.post("/users/register",json=user_json.dict())
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    user_dict = response.json()
    user_parse = parse_obj_as(generic.JsonRequest, user_dict)
    print(user_parse)
    assert user_parse.token != None
    assert user_parse.value["id"] != None

# def test_user_all():
#     response = router.get("/users/")
#     #response = httpx.post("/users/register",json=user_json.dict())
#     user_dict = response.json()
#     assert response.status_code == status.HTTP_200_OK
#     assert type(user_dict) == list