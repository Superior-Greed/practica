from typing import TypeVar, Generic
from sqlalchemy.orm import Session
from generic_crud import BaseService
from models.user import Role
from schema.user import RoleSchema
from schema.generic import JsonRequest
from datetime import datetime

T = TypeVar('T')

class Role_Service(BaseService):
    
    def insert_role(role:RoleSchema):
        new_role = Role()
        new_role.name = role.name
        new_role.description =role.description
        return new_role
    
    def exist_role(db:Session, model:Role,id:int):
      user = db.query(model).filter(model.id == id)
      if user.count() > 0:
          return user.first()
      return False

    def add_role(self,db:Session,role:Role):
        if not role.name.replace("  ",""):
            JsonRequest("no hay nombre",None)
        new_role = self.add(db,role)
        return new_role
    
    def remove_role(self,db:Session,id:int):
        role = self.exist_role(db,Role,id)
        if role != False:
            self.remove(db,role)
            return JsonRequest("Rol removido con exito",True)
        return JsonRequest("Rol no existe",None)