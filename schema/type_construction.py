from pydantic import BaseModel

class TypeConstructionSchema(BaseModel):
    id:int
    name:str
    description:str | None

