from pydantic import BaseModel

class Image_Construction(BaseModel):
    id: int
    description:str
    image:str | None