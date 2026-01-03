from fastapi import APIRouter, Depends, Request, HTTPException
from models import User
from dependencies import get_session
from fastapi.templating import Jinja2Templates
from main import bcrypt_context

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
async def create_account(email: str, password: str, name: str, user_id: str,session = Depends(get_session)):

    user = session.query(User).filter(User.email==email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        c_pass = bcrypt_context.hash(password)
        new_user = User(name, email, c_pass, user_id )
        session.add(new_user)
        session.commit()
        raise HTTPException(status_code=201, detail="Usuário criado com sucesso")


@auth_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/signIn.html",
        context={"request": request}
    )

@auth_router.post("/login")
async def login(request: Request):
    return{"message": "Login realizado com sucesso"}