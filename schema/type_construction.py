from pydantic import BaseModel
from schema import construction

class TypeConstructionSchema(BaseModel):
    id:int
    name:str
    description:str | None

