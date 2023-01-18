from pydantic import BaseModel

class Material(BaseModel):
    id: int
    name: str
    description: str | None
    # purchase_price:float |None
    # sell_price:float |None
    image: str|None