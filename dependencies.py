from fastapi import Depends, HTTPException
from models import User, db
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import ALGORITHM, SECRET_KEY, oauth2_schema

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def token_verification(token: str = Depends(oauth2_schema), session : Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) 
        user_id = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return user
