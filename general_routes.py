from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from schemas import LetterCreate, MarkLetterAsRead
from dependencies import get_session, token_verification, get_current_user
from models import Letter
from models import User
from sqlalchemy import desc


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
    nick_name = session.query(User).filter(User.user_name == letter_schema.user_name).first()

    if not nick_name:
        raise HTTPException(status_code=404, detail="Destinatário não encontrado. Verifique o apelido.")
    
    new_letter = Letter(recipient_id = nick_name.id, content = letter_schema.content, sender_id = current_user.id)
    session.add(new_letter)
    session.commit()
    raise  HTTPException(status_code=201, detail="Carta criada com sucesso")


@general_router.get("/letters/inbox")
async def get_inbox_letters(current_user = Depends(get_current_user), session = Depends(get_session)):

    letters = session.query(Letter, User).join(User, Letter.sender_id == User.id).filter(Letter.recipient_id == current_user.id).filter(Letter.status != "DRAFT")\
    .order_by(desc(Letter.id)).all()
    
    my_letters = []

    for letter, sender in letters:
    
        data_fmt = letter.created_at.strftime("%d/%m/%Y") if letter.created_at else "Data desc."
        
        my_letters.append({
            "uuid": letter.uuid,
            "sender_nick": sender.user_name,
            "created_at": data_fmt,
            "read": letter.is_read,
            "content": letter.content 
        })

    return my_letters


@general_router.patch("/mark_as_read")
async def mark_as_read(mark_schema : MarkLetterAsRead, session = Depends(get_session), current_user = Depends(get_current_user)):

    letter = session.query(Letter).filter(Letter.uuid == mark_schema.uuid, Letter.recipient_id == current_user.id).first()
    
    if not letter:
        raise HTTPException(status_code=404, detail="Carta não encontrada ou você não tem permissão para alterá-la")
    if letter.is_read == False and mark_schema.is_read == True:
        letter.is_read = True
    
    session.add(letter)
    session.commit()

    raise  HTTPException(status_code=201, detail="Status atualizado com sucesso")


@general_router.get("/inbox")
async def inbox(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request = request,
        name="inbox.html",
        context={"request": request}
    )


@general_router.get("/outbox")
async def outbox(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse(
        request = request,
        name="outbox.html",
        context={"request": request}
    )

@general_router.get("/letters/outbox")
async def get_outbox_letters(current_user = Depends(get_current_user), session = Depends(get_session)):
    letters = session.query(Letter, User).join(User, Letter.recipient_id == User.id).filter(Letter.sender_id == current_user.id).order_by(desc(Letter.id)).all()

    my_letters = []

    for letter, recipient in letters:
    
        created_fmt = letter.created_at.strftime("%d/%m/%Y") if letter.created_at else "Data desc."
        sent_fmt = letter.sent_at.strftime("%d/%m/%Y") if letter.sent_at else "Data desc."
        
        my_letters.append({
            "uuid": letter.uuid,
            "recipient_nick": recipient.user_name,
            "created_at": created_fmt,
            "status": letter.status,
            "sent_at": sent_fmt,
            "content": letter.content 
        })

    return my_letters