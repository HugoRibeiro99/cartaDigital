from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from schemas import LetterCreate
from dependencies import get_session
from models import Letter


templates = Jinja2Templates(directory="templates")


general_router = APIRouter(prefix="/app", tags=["/app"])

@general_router.get("/write_letter")
async def write_letter(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="write_letter.html",
        context={"request": request}
    )


@general_router.post("/write_letter")
async def write_letter(letter_schema : LetterCreate, session = Depends(get_session)):
    
    new_letter = Letter(recipient_id = letter_schema.recipient_id, content = letter_schema.content, sender_id = letter_schema.sender_id)
    session.add(new_letter)
    session.commit()
    raise  HTTPException(status_code=201, detail="Carta criada com sucesso")