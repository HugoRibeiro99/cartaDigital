from fastapi import APIRouter, Depends, Request
from models import User
from dependencies import get_session
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/create_account")
async def authenticate(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="auth/signUp.html",
        context={"request": request}
    )


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

@auth_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/signIn.html",
        context={"request": request}
    )