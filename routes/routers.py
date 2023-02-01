
from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from routes import users,role,type_construction,material,image,construction
from middleware.jwt_http import JwtMiddleware 


# user = APIRouter()

# @user.get("/")
# def root():
#     html_content = """
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look ma! HTML!</h1>
#         </body>
#     </html>
#     """
#     return HTTPResponse(content=html_content, status_code=200)

# class Item(BaseModel):
#     name:str
#     price:float
#     is_offer: Union[bool,None]=None

router = APIRouter()
router.include_router(users.user_route,prefix="/users",tags=["user"])
router.include_router(role.role_route,prefix="/role",tags=["role"])
router.include_router(type_construction.type_construction_route,prefix="/type_construction",tags=["type construction"])
router.include_router(material.material_route,prefix="/material",tags=["material"])
router.include_router(image.image_route,prefix="/images_construction",tags=["image"])
router.include_router(construction.construction_route,prefix="/construction",tags=["construction"])

# @router.get("/home", dependencies=[Depends(JwtMiddleware())])
# async def read_root():
#     return {"hello":"world"}


# @router.get("/items/{id}")
# async def read_item(id:int, q: Union[str,None] =None):
#     return {"id":id,"q":q}

# @app.put("/item/{id}")
# async def update_item(id:int,item:Item):
#     return {"item":item.name,"item_id":id}
