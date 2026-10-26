from fastapi import Depends, HTTPException
from models import db
from sqlalchemy.orm import sessionmaker, Session  
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from models import Usuario
from schemas import UsuarioSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Criar uma sessão no banco de dados
def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session() 
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY,ALGORITHM)
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido, verifique a data de expiração")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario