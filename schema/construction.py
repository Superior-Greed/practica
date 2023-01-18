from pydantic import BaseModel
from datetime import datetime
from schema import type_construction,image,material

class Construction(BaseModel):
    id : int
    name: str
    price: float | None
    init_date: datetime | None
    final_date: datetime | None
    id_type_construction:int
    type_construction: type_construction.Type_Construction | None
    images : list[image.Image_Construction] =[] | None
    materials: list[material.Material] = [] | None

