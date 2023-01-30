
from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import user as user_schema
from service import user as user_service
from models import user as user_model
from sqlalchemy.orm import Session
from config.db import get_db

user_route= APIRouter()
user_service = user_service.UserService()

@user_route.post("/")
async def user_login(user:user_schema.UserSchema,db:Session = Depends(get_db)):
    return user_service.register_user_token_or_insert_user(db,user_service.insert_user(user),False)

@user_route.post("/register")
async def user_register(users:user_schema.UserSchema,db:Session = Depends(get_db)):
    return user_service.register_user_token_or_insert_user(db,user_service.insert_user(users),True)

@user_route.post("/login")
async def user_login(users:user_schema.UserSchema,db:Session = Depends(get_db)):
    return user_service.login(db,user_service.insert_user(users))

@user_route.put("/{id}")
async def user_update(id:int,users:user_schema.UserSchema,db:Session = Depends(get_db)):
    return user_service.update_user(db,user_service.insert_user(users),id)

@user_route.delete("/{id}")
async def user_delete(id:int,db:Session = Depends(get_db)):
    return user_service.delete_user(db,id)

@user_route.get("/")
async def user_all(db:Session = Depends(get_db)):
    return user_service.all()

@user_route.get("/{id}")
async def user_filter(id:int,db:Session = Depends(get_db)):
    return user_service.filter(db,user_model.user,id)
