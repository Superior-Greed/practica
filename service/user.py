from typing import TypeVar, Generic
from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.user import User,UserRoles
from schema.user import UserSchema
from schema.generic import JsonRequest
from datetime import datetime
from service.jwt import JwtService
from sqlalchemy import or_,and_

T = TypeVar('T')


class UserService(BaseService):
    jwt = JwtService()

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
    def exist_user_email_name(db:Session, model:User,user_name:str,email:str):
        return db.query(model).filter(or_(model.user_name == user_name, model.email == email)).count() > 0
    
    @staticmethod
    def insert_user(user:UserSchema):
        new_user = User()
        new_user.user_name = user.user_name
        new_user.name = user.name.title()
        new_user.last_name = user.last_name.title()
        new_user.email = user.email
        new_user.password = user.password
        new_user.image = user.image
        new_user.session_init = datetime.utcnow
        return new_user
    
    @staticmethod
    def insert_user_schema(user:User):
        new_user = UserSchema(
        id = user.id,
        user_name = user.user_name,
        name = user.name,
        last_name = user.last_name,
        email = user.email,
        password = user.password,
        image = user.image)
        return new_user
    
    @staticmethod
    def validate_user(user:User):
        if(not user.email.replace(" ","")):
            return JsonRequest( error="no tiene email",value=None)
        
        if not user.user_name.replace(" ",""):
            return JsonRequest(error="no tiene el nombre de usuari", value=None)
        
        if not user.password.replace(" ",""):
            return JsonRequest(error="no hay contrasena", value=None)
        
        return JsonRequest(error="todo bien",value=True)
    
    #si es true genera registro y token si no solo agrega usuario
    def register_user_token_or_insert_user(self,db:Session,user:User,option:bool = False):
        validation = self.validate_user(user)
        if validation.value == None:
            return validation

        _user_name = self.exist_user_email_name(db,User,user.user_name,user.email)
        if(_user_name == False):

            user.password = self.jwt.password_hash(user.password)
            user.session_init = datetime.utcnow()
            new_user = self.add(db,user)
            if option == True:
                _userschema = self.insert_user_schema(user)
                token = JwtService.generate_toke(_userschema)
                if token == None:
                    return JsonRequest(error="usuario creado, problema con creacion de token",value=new_user)
                return JsonRequest(error="",value=new_user,token=token)
            return JsonRequest(error="",value=new_user)
        
        return JsonRequest(error="el usario ya existe",value=None)


    def delete_user(self,db:Session,id:int):
        user = self.exist_user(db,User,id)
        if(user != False):
            user_roles = db.query(UserRoles).filter(UserRoles.user_id == id)
            if user_roles.count()>0:
                user_roles.delete()
                db.commit()
            self.remove(db,user)
            return JsonRequest(error="borrado con exito",value=True)
        return JsonRequest(error="el usuario no existe",value=None)
    
    def update_user(self,db:Session,user:User,id:int):
        validation = self.validate_user(user)
        if validation.value == None:
            return validation
        
        if(self.exist_userid(db,User,id) ):
            user.password = self.jwt.password_hash (user.password)
            user.id = id
            db.query(User).filter(User.id == id).update({User.name : user.name , 
                                                        User.last_name : user.last_name, 
                                                        User.password : user.password,
                                                        User.image : user.image},synchronize_session=False)
            db.commit()
            return JsonRequest(error="actualizado con exito",value=self.insert_user_schema(user))
        return JsonRequest(error="El usuario a modificar no existe",value=None)
    
    def login(self,db:Session,user:User):
        _user = self.search_username(db,User,user.user_name)
        _userschema = self.insert_user_schema(_user)
        if _user == None:
            return JsonRequest(error="no existe el usario",value=None)
        if self.jwt.verify_password(user.password,_user.password) and _user.email == user.email.replace(" ",""):
            return JsonRequest(error="",value=_userschema,token=JwtService.generate_toke(_userschema))
        return JsonRequest(error="contrasena o correo incorrecto",value=None)