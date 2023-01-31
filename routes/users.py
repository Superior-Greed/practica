
from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import user as user_schema
from service import roles as role_service, user as user_service,jwt
from models import user as user_model 
from sqlalchemy.orm import Session
from config.db import get_db

user_route= APIRouter()
_user_service = user_service.UserService()
_role_service = role_service.RoleService()
auth_handler = jwt.JwtService()

@user_route.post("/create",dependencies=[Depends(auth_handler.auth_token)])
async def user_create(user:user_schema.UserSchema,db:Session = Depends(get_db)):
    return _user_service.register_user_token_or_insert_user(db,_user_service.insert_user(user),False)

@user_route.post("/register")
async def user_register(users:user_schema.UserSchema,db:Session = Depends(get_db)):
    _user = _user_service.insert_user(users)
    return _user_service.register_user_token_or_insert_user(db,_user, True)

@user_route.post("/login")
async def user_login(users:user_schema.UserSchema,db:Session = Depends(get_db)):
    return _user_service.login(db,_user_service.insert_user(users))

@user_route.put("/{id}")
async def user_update(id:int,users:user_schema.UserSchema,db:Session = Depends(get_db),user_name = Depends(auth_handler.auth_token)):
    return _user_service.update_user(db,_user_service.insert_user(users),id)

@user_route.delete("/{id}")
async def user_delete(id:int,db:Session = Depends(get_db),user_name = Depends(auth_handler.auth_token)):
    return _user_service.delete_user(db,id)

@user_route.get("/")
async def user_all(db:Session = Depends(get_db),user_name = Depends(auth_handler.auth_token)):
    return _user_service.all(db,user_model.User)

@user_route.get("/{id}")
async def user_filter(id:int,db:Session = Depends(get_db),user_name = Depends(auth_handler.auth_token)):
    return _user_service.filter(db,user_model.User,id)

@user_route.get("/users_role/{id_user}")
async def user_role_filter(id_user:int,db:Session = Depends(get_db)):
    return _role_service.filter_role_user(db,id_user)

@user_route.post("/user_role")
async def user_add_role(user_role:user_schema.UserRoleSchema,db:Session = Depends(get_db)):
    return _role_service.add_role_user(db,user_role.role_id,user_role.user_id)

@user_route.get("/user_role/all")
async def user_role_all(db:Session = Depends(get_db)):
    return _role_service.all_role_user(db)

@user_route.delete("/{id_user}/{id_role}")
async def user_delete_role(id_user:int,id_role:int,db:Session = Depends(get_db)):
    return _role_service.remove_role_user(db,id_role,id_user)