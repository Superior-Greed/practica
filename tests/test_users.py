from fastapi.testclient import TestClient
from pydantic.tools import parse_obj_as
from fastapi import status
from schema.user import UserSchema
from schema.generic import JsonRequest
from main import app
import json
import httpx

router = TestClient(app=app)
token_falso = JsonRequest(error="",value="",token="")
# def test_user_register():
#     user_json:UserSchema = UserSchema(
#         id=0,
#         user_name="prueba",
#         email="prueba1@gmail.com",
#         name= "prueba",
#         last_name= "prueba",
#         password= "prueba"
#     )
#     response = router.post("/users/register",json=user_json.dict())
#     #response = httpx.post("/users/register",json=user_json.dict())
#     user_dict = response.json()
#     user_parse = parse_obj_as(JsonRequest, user_dict)
#     print(response.status_code)
#     print(user_parse)
#     print(response.status_code == status.HTTP_200_OK)
#     token = user_parse.token
#     assert response.status_code == status.HTTP_200_OK
#     assert user_parse.token != None
#     assert user_parse.value["id"] != None

def test_user_login():
    user_json:UserSchema = UserSchema(
        id=0,
        user_name="prueba",
        email="prueba@gmail.com",
        name= "prueba",
        last_name= "prueba",
        password= "prueba123"
        )
    response = router.post("/users/login",json=user_json.dict())
    assert response.status_code == status.HTTP_200_OK
    user_parse = parse_obj_as(JsonRequest, response.json())
    token_falso.token = user_parse.token
    assert user_parse.token != None

def test_user_all():
    print(token_falso.token)
    token ={
      "Authorization": "Bearer {0}".format(token_falso.token)
    }
    response = router.get("/users/",headers=token)
    #response = httpx.post("/users/register",json=user_json.dict())
    user_dict =  response.json()
    print(user_dict)
    assert response.status_code == status.HTTP_200_OK
    assert type(user_dict) == list