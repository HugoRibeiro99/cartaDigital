from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from schemas import LetterCreate
from dependencies import get_session, token_verification, get_current_user
from models import Letter
from models import User


templates = Jinja2Templates(directory="templates")


general_router = APIRouter(prefix="/app", tags=["/app"])

@general_router.get("/write_letter")
async def write_letter(request: Request, user = Depends(get_current_user)):

    return templates.TemplateResponse(
        request = request,
        name="write_letter.html",
        context={"request": request}
    )


@general_router.post("/write_letter")
async def write_letter(letter_schema : LetterCreate, current_user = Depends(get_current_user), session = Depends(get_session)):
    'fazer logica getByID para verificar se o recipient existe'
    nick_name = session.query(User).filter(User.user_id == letter_schema.recipient_user_id).first()

    if not nick_name:
        raise HTTPException(status_code=404, detail="Destinatário não encontrado. Verifique o apelido.")
    
    new_letter = Letter(recipient_id = nick_name.id, content = letter_schema.content, sender_id = current_user.id)
    session.add(new_letter)
    session.commit()
    raise  HTTPException(status_code=201, detail="Carta criada com sucesso")


@general_router.get("/inbox")
async def inbox(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="inbox.html",
        context={"request": request}
    )


@general_router.get("/outbox")
async def outbox(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="outbox.html",
        context={"request": request}
    )