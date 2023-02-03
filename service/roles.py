from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.user import Role, UserRoles,User
from schema.user import RoleSchema
from schema.generic import JsonRequest
from sqlalchemy import or_,and_

class RoleService(BaseService):
    
    @staticmethod
    def insert_role(role:RoleSchema):
        new_role = Role()
        new_role.name = role.name.title()
        new_role.description = role.description
        return new_role

    @staticmethod
    def insert_role_schema(role:Role):
        new_role = RoleSchema(
            id=role.id,
            name=role.name,
            description=role.description
        )
        return new_role
    
    @staticmethod
    def exist_role(db:Session, model:Role,id:int):
      user = db.query(model).filter(model.id == id)
      if user.count() > 0:
          return user.first()
      return False
    
    @staticmethod
    def exist_role_name(db:Session, model:Role,name:str):
      user = db.query(model).filter(model.name == name)
      if user.count() > 0:
          return user.first()
      return False

    def add_role(self,db:Session,role:Role):
        if not role.name.replace(" ",""):
            JsonRequest(error="no hay nombre",value=None)
        if self.exist_role_name(db,Role,role.name):
            return JsonRequest(error="ya existe",value=None)
        new_role = self.add(db,role)
        return JsonRequest(error="rol agregado co exito",value=new_role)
    
    def remove_role(self,db:Session,id:int):
        role = self.exist_role(db,Role,id)
        if role != False:
            user_roles = db.query(UserRoles).filter(UserRoles.roles_id == id)
            if user_roles.count()>0:
                user_roles.delete() 
                db.commit()
            self.remove(db,role)
            return JsonRequest(error="Rol removido con exito",value=True)
        return JsonRequest(error="Rol no existe",value=None)
    
    def update_role(self,db:Session,id:int,model:Role):
        role = self.exist_role(db,Role,id)
        if role != False:
            db.query(Role).filter(Role.id == id).update({
                Role.description : model.description
            },synchronize_session=False)
            db.commit()
            return JsonRequest(error="Rol removido con exito",value=self.insert_role_schema(model))
        return JsonRequest(error="Rol no existe",value=None)
    
    @staticmethod
    def validate_user_role_exist(db:Session,role_id:int,user_id:int):
        if db.query(Role).filter(Role.id == role_id).count()==0:
            return JsonRequest(error="no existe el rol",value=True)
        if db.query(User).filter(User.id == user_id).count()==0:
            return JsonRequest(error="no existe el usaurio",value=True)
        return JsonRequest(error="existe",value=False)
    
    def add_role_user(self,db:Session,role_id:int,user_id:int):
        not_exist = self.validate_user_role_exist(db,role_id,user_id)
        if not_exist.value:
            return not_exist
        user_role = UserRoles()
        user_role.user_id = user_id
        user_role.roles_id = role_id
        return JsonRequest(error="agregado con exito", value= self.add(db,user_role))
    
    def remove_role_user(self,db:Session,role_id:int,user_id:int):
        not_exist = self.validate_user_role_exist(db,role_id,user_id)
        if not_exist.value:
            return not_exist
        user_role = db.query(UserRoles).filter(and_(UserRoles.user_id == user_id ,UserRoles.roles_id == role_id))
        if user_role.count() > 0:
            self.remove(db,user_role.first())
            return JsonRequest(error="removido con exito",value=True)
        return JsonRequest(error="no existe el usuario con ese rol",value=False)
    
    def all_role_user(self,db:Session):
        return db.query(UserRoles,Role,User).join(UserRoles.users).join(UserRoles.roles).all()

    def filter_role_user(self,db:Session,user_id:int):
        user_role = db.query(UserRoles,Role,User).join(UserRoles.users).join(UserRoles.roles).filter(UserRoles.user_id == user_id).all()
        if len(user_role) > 0:
            return JsonRequest(error="no existe el usuario con ese rol",value=user_role)
        return JsonRequest(error="no existe el usuario con ese rol",value=False)
