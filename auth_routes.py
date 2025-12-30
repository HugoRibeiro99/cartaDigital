from fastapi import APIRouter, Depends
from models import User
from dependencies import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
    return {"mensagem: Voce acessou a rota AUTH"}


@auth_router.post("/create_account")
async def create_account(email: str, password: str, name: str, session = Depends(get_session)):

    user = session.query(User).filter(User.email==email).first()
    
    if user:
        return {"mensagem": "Email ja cadastrado"}
    else:
        new_user = User(name, email, password)
        session.add(new_user)
        session.commit()
        return {"mensagem": "Conta criada com sucesso"}

    session.close()