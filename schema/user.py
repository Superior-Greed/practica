from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    user_name:str
    name:str
    last_name: str
    email: str
    password:str
    image:str | None
    session_init:datetime | None

class Role(BaseModel):
    id:int
    name:str
    description:str | None

class UserRole(BaseModel):
    id_user:int
    users: list[User] = [] | None
    id_role:int
    roles: list[Role] = [] | None