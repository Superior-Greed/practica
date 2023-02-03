from fastapi.testclient import TestClient
from pydantic.tools import parse_obj_as
from fastapi import status
from schema.user import UserSchema,RoleSchema,UserRoleSchema
from schema.generic import JsonRequest
from tests.token import tokenJson
from main import app
import json
import httpx

router = TestClient(app=app)

user_final = UserSchema(id=0,
            user_name="prueba_final",
            email="prueba_final@gmail.com",
            name= "prueba3",
            last_name= "prueba3",
            password= "prueba123")
role_final = RoleSchema( 
    id=0,
    description= "f",
    name="prueba")

def test_user_register():
    user_json:UserSchema = UserSchema(
            id=0,
            user_name="prueba_final",
            email="prueba_final@gmail.com",
            name= "prueba3",
            last_name= "prueba3",
            password= "prueba123"
            )
    response = router.post("/users/register",json=user_json.dict())
    #response = httpx.post("/users/register",json=user_json.dict())
    user_dict = response.json()
    user_parse = parse_obj_as(JsonRequest, user_dict)
    tokenJson.token_save(user_parse)
    assert response.status_code == status.HTTP_200_OK
    assert user_parse.token != None
    assert user_parse.value["id"] != None

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
    user_parse = parse_obj_as(JsonRequest, response.json())
    tokenJson.token_save(user_parse)
    assert response.status_code == status.HTTP_200_OK
    assert user_parse.token != None

def test_user_create():
    user_json:UserSchema = UserSchema(
            id=0,
            user_name="prueba8",
            email="prueba8@gmail.com",
            name= "prueba",
            last_name= "prueba",
            password= "prueba123"
            )
    response = router.post("/users/create",json=user_json.dict(),headers=tokenJson.token_read())
    user_dict = response.json()
    user_parse = parse_obj_as(JsonRequest, user_dict)
    user_final.id = user_parse.value["id"]
    assert response.status_code == status.HTTP_200_OK
    assert user_parse.token == None
    assert user_parse.value["id"] != None

def test_user_all():
    response = router.get("/users/",headers=tokenJson.token_read())
    user_dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert type(user_dict) == list
    assert len(user_dict) > 0

def test_user_filter():
    response = router.get("/users/{0}".format(user_final.id),headers=tokenJson.token_read())
    user = parse_obj_as(UserSchema, response.json())
    assert response.status_code == status.HTTP_200_OK
    assert user.id > 0

def test_role_add():
    role_json:RoleSchema = RoleSchema(
            id=0,
            description= "f",
            name="prueba"
            )
    response = router.post("/role/",json=role_json.dict(),headers=tokenJson.token_read())
    role_dict = response.json()
    role_parse = parse_obj_as(JsonRequest, role_dict)
    role_final.id = role_parse.value["id"]
    assert response.status_code == status.HTTP_200_OK
    assert role_parse.token == None
    assert role_parse.value["id"] != None

def test_role_filter():
    response = router.get("/role/{0}".format(role_final.id),headers=tokenJson.token_read())
    role = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert role["id"] > 0

def test_role_update():
    role_final.name = "falso"
    role_final.description = "falso"
    response = router.put("/role/{0}".format(role_final.id),json=role_final.dict(),headers=tokenJson.token_read())
    role = parse_obj_as(JsonRequest, response.json())
    assert response.status_code == status.HTTP_200_OK
    assert role.value["description"] == role_final.description

def test_user_role_create():
    user_json:UserRoleSchema = UserRoleSchema(
        role_id= role_final.id,
        user_id= user_final.id
        )
    response = router.post("/users/user_role",json=user_json.dict(),headers=tokenJson.token_read())
    assert response.status_code == status.HTTP_200_OK

def test_role_delete():
    response = router.delete("/role/{0}".format(role_final.id),headers=tokenJson.token_read())
    assert response.status_code == status.HTTP_200_OK

def test_user_delete():
    response = router.delete("/users/{0}".format(user_final.id),headers=tokenJson.token_read())
    user = parse_obj_as(JsonRequest, response.json())
    assert response.status_code == status.HTTP_200_OK
    assert user.value