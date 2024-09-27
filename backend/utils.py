from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os

security = HTTPBearer()


# Leer la clave privada desde la variable de entorno
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
if(PUBLIC_KEY is None):
    PUBLIC_KEY = "public"


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        # Decodificar el token usando la clave pública
        payload = jwt.decode(credentials.credentials, PUBLIC_KEY, algorithms=["RS256"])
        return payload  # Devuelve el payload si es válido
    except jwt.JWTError:
        # Si el token no es válido, lanza una excepción
        raise HTTPException(status_code=401, detail="Invalid or expired token")