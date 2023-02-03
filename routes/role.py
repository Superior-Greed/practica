from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import user as role_schema
from service import roles as role_service,jwt
from models import user as role_model 
from sqlalchemy.orm import Session
from config.db import get_db

role_route= APIRouter()
_role_service = role_service.RoleService()

auth_handler = jwt.JwtService()

@role_route.get("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_all(db:Session = Depends(get_db)):
    return _role_service.all(db,role_model.Role)

@role_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_filter(id:int,db:Session = Depends(get_db)):
    return _role_service.filter(db,role_model.Role,id)

@role_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_create(role:role_schema.RoleSchema,db:Session = Depends(get_db)):
    return _role_service.add_role(db,_role_service.insert_role(role))

@role_route.delete("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_delete(id:int,db:Session = Depends(get_db)):
    return _role_service.remove_role(db,id)

@role_route.put("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_update(id:int,role:role_schema.RoleSchema,db:Session = Depends(get_db)):
    return _role_service.update_role(db,id,role)
