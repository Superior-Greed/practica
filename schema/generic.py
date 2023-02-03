from pydantic import BaseModel
from typing import Generic,TypeVar

T = TypeVar('T')

class JsonRequest(BaseModel,Generic[T]):
    error : str
    value : T
    token : str | None