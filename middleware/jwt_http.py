
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from service.jwt import SECRET_KEY,ALGORITHM
from jose import jwt

class JwtMiddleware(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JwtMiddleware, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtMiddleware, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="esquema de token invalido")
            if self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="token expirado")
            return credentials.credentials
        else:
            raise HTTPException(
                status=403, detail="codigo de autitentificacion invalido")

    def verfity_jwt(Self, jwttoken: str):
        isTokenValid: bool = False

        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithm=[ALGORITHM])
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid