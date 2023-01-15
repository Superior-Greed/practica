from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name:str
    price:float
    is_offer: Union[bool,None]=None

app = FastAPI()

@app.get("/")
async def read_root():
    return {"hello":"world"}


@app.get("/items/{id}")
async def read_item(id:int, q: Union[str,None] =None):
    return {"id":id,"q":q}

@app.put("/item/{id}")
async def update_item(id:int,item:Item):
    return {"item":item.name,"item_id":id}
