from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import material as material_schema
from service import material as material_service,jwt
from models import fences as material_model 
from sqlalchemy.orm import Session
from config.db import get_db

material_route= APIRouter()
_material_service = material_service.MaterialService()

auth_handler = jwt.JwtService()

@material_route.get("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_all(db:Session = Depends(get_db)):
    return _material_service.all(db,material_model.Material)

@material_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_filter(id:int,db:Session = Depends(get_db)):
    return _material_service.filter(db,material_model.Material,id)

@material_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_create(type_constructio:material_schema.MaterialSchema,db:Session = Depends(get_db)):
    return _material_service.add_material(db,_material_service.insert_type_costruction(type_constructio))

@material_route.delete("/{id}")
async def role_delete(id:int,db:Session = Depends(get_db)):
    return _material_service.remove_material(db,id)

@material_route.put("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_update(id:int,type_constructio:material_schema.MaterialSchema,db:Session = Depends(get_db)):
    return _material_service.update_material(db,type_constructio,id)
