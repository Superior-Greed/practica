from fastapi.testclient import TestClient
from fastapi import status
from main import app

from pydantic.tools import parse_obj_as
from schema import user,generic
import json
import httpx

router = TestClient(app=app)



def test_user_all():
    response = router.get("/users/")
    #response = httpx.post("/users/register",json=user_json.dict())
    user_dict = response.json()
    assert response.status_code != status.HTTP_200_OK