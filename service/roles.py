from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.user import Role, UserRoles,User
from schema.user import RoleSchema
from schema.generic import JsonRequest


class RoleService(BaseService):
    
    def insert_role(role:RoleSchema):
        new_role = Role()
        new_role.name = role.name.title()
        new_role.description = role.description
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
        return JsonRequest("rol agregado co exito",new_role)
    
    def remove_role(self,db:Session,id:int):
        role = self.exist_role(db,Role,id)
        if role != False:
            user_roles = db.query(UserRoles).filter(UserRoles.roles_id == id)
            if user_roles.count()>0:
                user_roles.delete() 
            self.remove(db,role)
            return JsonRequest("Rol removido con exito",True)
        return JsonRequest("Rol no existe",None)
    
    def validate_user_role_exist(db:Session,role_id:int,user_id:int):
        if db.query(Role).filter(Role.id == role_id).count()==0:
            return JsonRequest("no existe el rol",True)
        if db.query(User).filter(User.id == user_id).count()==0:
            return JsonRequest("no existe el usaurio",True)
        return JsonRequest("existe",False)
    
    def add_role_user(self,db:Session,role_id:int,user_id:int):
        not_exist = self.validate_user_role_exist(db,role_id,user_id)
        if not_exist.value:
            return not_exist
        user_role = UserRoles()
        user_role.user_id = user_id
        user_role.roles_id = role_id
        return JsonRequest("agregado con exito",  self.add(db,user_role))
    
    def remove_role_user(self,db:Session,role_id:int,user_id:int):
        not_exist = self.validate_user_role_exist(db,role_id,user_id)
        if not_exist.value:
            return not_exist
        user_role = db.query(UserRoles).filter(UserRoles.user_id == user_id & UserRoles.roles_id == role_id)
        if user_role.count() > 0:
            self.remove(user_role.first())
            return JsonRequest("removido con exito",True)
        return JsonRequest("no existe el usuario con ese rol",False)