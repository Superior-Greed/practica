from datetime import datetime
from pydantic import BaseModel #,EmailStr

#email cambiar str por email
#session_init poner optional[datetime]
class UserSchema(BaseModel):
    id: int
    user_name:str
    name:str
    last_name: str
    email: str#EmailStr
    password:str
    image:str | None
    #session_init:datetime | None

class RoleSchema(BaseModel):
    id:int
    name:str
    description:str | None

class UserRoleSchema(BaseModel):
    user_id:int
    role_id:int