from pydantic import BaseModel
from typing import Generic,TypeVar

T = TypeVar('T')

class JsonRequest(BaseModel):
    error : str
    value : Generic[T]
    token : str | None