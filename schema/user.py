from datetime import datetime
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    user_name:str
    name:str
    last_name: str
    email: str
    password:str
    image:str | None
    session_init:datetime | None

class RoleSchema(BaseModel):
    id:int
    name:str
    description:str | None

class UsersRolesSchema(BaseModel):
    id_user:int
    users: list[UserSchema] = [] 
    id_role:int
    roles: list[RoleSchema] = [] 

class UserRolesSchema(BaseModel):
    id_user:int
    user: UserSchema
    id_role:int
    roles:list [RoleSchema] = [] 