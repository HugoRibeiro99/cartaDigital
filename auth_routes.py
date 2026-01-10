from fastapi import APIRouter, Depends, Request, HTTPException
from models import User
from dependencies import get_session, token_verification
from fastapi.templating import Jinja2Templates
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

templates = Jinja2Templates(directory="templates")

auth_router = APIRouter(prefix="/auth", tags=["auth"])



def user_auth(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_token(user_id, duration_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dict_info = {"sub" : str(user_id), "exp": expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


@auth_router.get("/create_account")
async def authenticate(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="auth/signUp.html",
        context={"request": request}
    )


@auth_router.post("/create_account")
async def create_account(user_schema : UserSchema, session = Depends(get_session)):

    user = session.query(User).filter(User.email==user_schema.email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        c_pass = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, c_pass, user_schema.user_id )
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
async def login(login_schema : LoginSchema, session = Depends(get_session)):
    user = user_auth(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais invalidas")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token=timedelta(days=7))
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.post("/login-form")
async def login_form(data_form: OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)):
    user = user_auth(data_form.username, data_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais invalidas")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token, 
            "token_type": "Bearer"
        }  



@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(token_verification)):

    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }