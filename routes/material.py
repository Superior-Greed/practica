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
async def material_all(db:Session = Depends(get_db)):
    return _material_service.all(db,material_model.Material)

@material_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def material_filter(id:int,db:Session = Depends(get_db)):
    return _material_service.filter(db,material_model.Material,id)

@material_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def material_create(material:material_schema.MaterialSchema,db:Session = Depends(get_db)):
    return _material_service.add_material(db,_material_service.insert_materials(material))

@material_route.delete("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def material_delete(id:int,db:Session = Depends(get_db)):
    return _material_service.remove_material(db,id)

@material_route.put("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def material_update(id:int,material:material_schema.MaterialSchema,db:Session = Depends(get_db)):
    return _material_service.update_material(db,material,id)
