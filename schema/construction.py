from pydantic import BaseModel
from datetime import datetime
from schema import type_construction,image,material
from typing import Generic,TypeVar

T = TypeVar('T')
class ConstructionSchema(BaseModel):
    id : int
    name: str
    price: float | None
    init_date: datetime | None
    final_date: datetime | None
    id_type_construction:int
    # type_construction: type_construction.TypeConstructionSchema | None
    # images : list[image.ImageConstructionSchema] =[] | None
    # materials: list[material.MaterialSchema] = [] | None

