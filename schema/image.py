from pydantic import BaseModel

class ImageConstructionSchema(BaseModel):
    id: int
    description:str
    image:str | None