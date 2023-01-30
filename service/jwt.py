from datetime import timedelta,datetime
from typing import Optional
from jose import jwt,JWTError,ExpiredSignatureError
from schema.user import UserSchema
from fastapi import HTTPException,Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

SECRET_KEY="Greed"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180   

class JwtService():

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

    def password_hash(self,password:str):
        return self.pwd_context.hash(password)
    
    def verify_password(self, password:str ,hash_password:str):
        return self.pwd_context.verify(password,hash_password)

    def generate_toke(data:UserSchema,expire:Optional[timedelta]=ACCESS_TOKEN_EXPIRE_MINUTES):
        if data != None:
            encode = {
                "sub": data.user_name,
                "exp": datetime.utcnow() + timedelta(minutes=expire),
                "iat": datetime.utcnow()
            }
            encode_jwt = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
            return encode_jwt
        return None
    
    def decode_token(self,token:str):
        try:
            decode_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            return decode_token 
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=401,detail=e)
    
    def auth_token(self,auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
    
    # def generate_token(data:dict,expire:Optional[timedelta]=ACCESS_TOKEN_EXPIRE_MINUTES):
    #     if data == None:
    #         return {"token":None, "error":"fatal el data"}
    #     encode = data.copy()
    #     expire_token = datetime.utcnow + expire
    #     encode.update({"exp":expire_token})
    #     encode_jwt = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    #     return {"token":encode_jwt, "error":""}
    