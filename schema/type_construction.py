from pydantic import BaseModel
from schema import construction

class Type_Construction(BaseModel):
    id:int
    name:str
    description:str | None

