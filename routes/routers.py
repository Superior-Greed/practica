
from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from routes import users,role,type_construction,material,image,construction
from middleware.jwt_http import JwtMiddleware 

router = APIRouter()
router.include_router(users.user_route,prefix="/users",tags=["user"])
router.include_router(role.role_route,prefix="/role",tags=["role"])
router.include_router(type_construction.type_construction_route,prefix="/type_construction",tags=["type construction"])
router.include_router(material.material_route,prefix="/material",tags=["material"])
router.include_router(image.image_route,prefix="/images_construction",tags=["image"])
router.include_router(construction.construction_route,prefix="/construction",tags=["construction"])

