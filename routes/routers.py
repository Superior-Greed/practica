
from fastapi import APIRouter,Depends
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from routes import users
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
router.include_router(users.user_route)
# @router.get("/home", dependencies=[Depends(JwtMiddleware())])
# async def read_root():
#     return {"hello":"world"}


# @router.get("/items/{id}")
# async def read_item(id:int, q: Union[str,None] =None):
#     return {"id":id,"q":q}

# @app.put("/item/{id}")
# async def update_item(id:int,item:Item):
#     return {"item":item.name,"item_id":id}
