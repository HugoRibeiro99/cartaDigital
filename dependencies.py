from fastapi import Depends, HTTPException, Request, status
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



def get_current_user(request: Request, session: Session = Depends(get_session)):
   
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header
        else:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, 
                detail="Usuário não autenticado, redirecionando para login",
                headers={"Location": "/auth/login"}
            )

    
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) 
        user_id : str = dic_info.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail="Token inválido",
                headers={"Location": "/auth/login"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Token expirado, redirecionando para login",
            headers={"Location": "/auth/login"}
        )
    
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Usuário não encontrado, redirecionando para login",
            headers={"Location": "/auth/login"}
        )

    return user
