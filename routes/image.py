from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from schema import image as image_schema
from service import image as image_service,jwt
from models import fences as image_model 
from sqlalchemy.orm import Session
from config.db import get_db

image_route= APIRouter()
_image_service = image_service.ImageConstructionService()

auth_handler = jwt.JwtService()

@image_route.get("/",dependencies=[Depends(auth_handler.auth_token)])
async def image_all(db:Session = Depends(get_db)):
    return _image_service.all(db,image_model.ImageConstruction)

@image_route.get("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def image_filter(id:int,db:Session = Depends(get_db)):
    return _image_service.filter(db,image_model.ImageConstruction,id)

@image_route.post("/",dependencies=[Depends(auth_handler.auth_token)])
async def image_create(images:list[image_schema.ImageConstructionSchema],db:Session = Depends(get_db)):
    return _image_service.add_all_image_construction(db,_image_service.insert_image_construction(images))

@image_route.delete("/{id}",dependencies=[Depends(auth_handler.auth_token)])
async def image_delete(id:int,db:Session = Depends(get_db)):
    return _image_service.remove_image_construction(db,id)

