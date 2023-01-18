from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel



user = APIRouter()

@user.get("/")
def root():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTTPResponse(content=html_content, status_code=200)

class Item(BaseModel):
    name:str
    price:float
    is_offer: Union[bool,None]=None

app = FastAPI()

@app.get("/home")
async def read_root():
    return {"hello":"world"}


@app.get("/items/{id}")
async def read_item(id:int, q: Union[str,None] =None):
    return {"id":id,"q":q}

@app.put("/item/{id}")
async def update_item(id:int,item:Item):
    return {"item":item.name,"item_id":id}
