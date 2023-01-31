from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import type_construction as type_construction_schema
from service import type_construction as type_construction_service,jwt
from models import fences as type_construction_model 
from sqlalchemy.orm import Session
from config.db import get_db

type_construction_route= APIRouter()
_type_construction_service = type_construction_service.TypeConstructioService()

auth_handler = jwt.JwtService()

@type_construction_route.get("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_all(db:Session = Depends(get_db)):
    return _type_construction_service.all(db,type_construction_model.TypeConstruction)

@type_construction_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_filter(id:int,db:Session = Depends(get_db)):
    return _type_construction_service.filter(db,type_construction_model.TypeConstruction,id)

@type_construction_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def role_create(type_constructio:type_construction_schema.TypeConstructionSchema,db:Session = Depends(get_db)):
    return _type_construction_service.add_type_construction(db,_type_construction_service.insert_type_costruction(type_constructio))

@type_construction_route.delete("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_delete(id:int,db:Session = Depends(get_db)):
    return _type_construction_service.delete_type_costruction(db,id)

@type_construction_route.put("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def role_update(id:int,type_constructio:type_construction_schema.TypeConstructionSchema,db:Session = Depends(get_db)):
    return _type_construction_service.update_type_construction(db,type_constructio,id)
