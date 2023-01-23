from typing import TypeVar, Generic
from sqlalchemy.orm import Session
from generic_crud import BaseService
from models.user import User,UserRoles
from schema.user import UserSchema
from schema.generic import JsonRequest
from datetime import datetime
from service.jwt import JwtService

T = TypeVar('T')


class User_Service(BaseService):
    
    @staticmethod
    def search_username(db:Session, model:Generic[T],name:str):
        return db.query(model).filter(model.user_name == name).first()
        
    @staticmethod
    def search_userid(db:Session, model:Generic[T],id:int):
        return db.query(model).filter(model.id == id).first()
    
    @staticmethod
    def exist_user(db:Session, model:User,id:int):
      user = db.query(model).filter(model.id == id)
      if user.count() > 0:
          return user.first()
      return False

    @staticmethod
    def exist_userid(db:Session,model:User,id:int):
        return db.query(model).filter(model.id == id).count() > 0

    @staticmethod
    def exist_user(db:Session, model:User,name:str,email:str):
        return db.query(model).filter(model.name == name or model.email == email).count() > 0
    
    def insert_user(user:UserSchema):
        new_user = User()
        new_user.user_name = user.user_name
        new_user.name = user.name
        new_user.last_name = user.last_name
        new_user.email = user.email
        new_user.password = user.password
        new_user.image = user.image
        return new_user
    
    def validate_user(self,user:User):
        if(user.email == None):
            return JsonRequest("no tiene email",None)
        
        if(user.user_name == None):
            return JsonRequest("no tiene el nombre de usuari", None)
        
        if not user.password.replace("  ",""):
            return JsonRequest("no hay contrasena", None)
        
        return True
    
    # def insert_user(self,db:Session,user:User):
    #     validation = self.validate_user(db,user)
    #     if validation.value == None:
    #         return validation
        
    #     _user_name = self.exist_user(db,user,user.name,user.email)
    #     if(_user_name == False):
    #         user.password = JwtService.password_hash(user.password)
    #         user.session_init = datetime.utcnow()
    #         new_user = self.add(db,user)
    #         return JsonRequest("",new_user)
        
    #     return JsonRequest("el usario ya existe",None)
    
    #si es true genera registro y token si no solo agrega usuario
    def register_user_token_or_insert_user(self,db:Session,user:User,option:bool):
        validation = self.validate_user(db,user)
        if validation.value == None:
            return validation
        
        _user_name = self.exist_user(db,user,user.name,user.email)
        if(_user_name == False):
            user.password = JwtService.password_hash(user.password)
            user.session_init = datetime.utcnow()
            new_user = self.add(db,user)
            if option:
                token = JwtService.generate_toke(user)
                if token == None:
                    return JsonRequest("usuario creado, problema con creacion de token",new_user)
                return JsonRequest("",new_user,token)
            return JsonRequest("",new_user)
        
        return JsonRequest("el usario ya existe",None)


    def delete_user(self,db:Session,id:int):
        user = self.exist_user(db,User,id)
        if(user != True):
            self.remove(db,user)
            return JsonRequest("",True)
        return JsonRequest("el usuario no existe",None)
    
    def update_user(self,db:Session,user:User,id:int):
        validation = self.validate_user(db,user)
        if validation.value == None:
            return validation
        
        if(self.exist_userid(db,user,id) ):
            self.update(db,user,id)
            return JsonRequest("",user)
        return JsonRequest("El usuario a modificar no existe",None)
    
    def add_role_user(self,db:Session,user_id:int,role_id:int):
        user_role = UserRoles()
        user_role.user_id = user_id
        user_role.roles_id = role_id
        return self.add(user_role)