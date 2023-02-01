from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import construction as construction_schema
from service import construction as construction_service,jwt
from models import fences as construction_model 
from sqlalchemy.orm import Session
from config.db import get_db

construction_route= APIRouter()
_construction_service = construction_service.ConstructionService()

auth_handler = jwt.JwtService()

@construction_route.get("/",dependencies=[Depends(auth_handler.auth_token)])
async def construction_all(db:Session = Depends(get_db)):
    return _construction_service.all(db,construction_model.Construction)

@construction_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def construction_filter(id:int,db:Session = Depends(get_db)):
    return _construction_service.filter(db,construction_model.Construction,id)

@construction_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def construction_create(constructions:construction_schema.ConstructionSchema,db:Session = Depends(get_db)):
    return _construction_service.add_construction(db,_construction_service.insert_construction(constructions))

@construction_route.delete("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def construction_delete(id:int,db:Session = Depends(get_db)):
    return _construction_service.delete_construction(db,id)

@construction_route.put("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def construction_update(id:int,construction:construction_schema.ConstructionSchema,db:Session = Depends(get_db)):
    return _construction_service.update_construction(db,_construction_service.insert_construction(construction),id)
    
@construction_route.get("/construction_material/",dependencies=[Depends(auth_handler.auth_token)])
async def construction_material_create(db:Session = Depends(get_db)):
    return _construction_service.all(db,construction_model.ConstructionMaterial)

@construction_route.get("/construction_material/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def construction_material_create(id:int,db:Session = Depends(get_db)):
    return _construction_service.filter_construction_material(db,id)

@construction_route.post("/construction_material/",dependencies=[Depends(auth_handler.auth_token)])
async def construction_material_create(construction_id:int,material_id:int,db:Session = Depends(get_db)):
    return _construction_service.add_construction_material(db,construction_id,material_id)

@construction_route.delete("/construction_material/{construction_id}/{material_id}",dependencies=[Depends(auth_handler.auth_token)])
async def construction_material_delete(construction_id:int,material_id:int,db:Session = Depends(get_db)):
    return _construction_service.delete_construction_material(db,construction_id,material_id)
