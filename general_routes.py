from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")


general_router = APIRouter(prefix="/app", tags=["/app"])

@general_router.get("/write_letter")
async def write_letter(request: Request):
    return templates.TemplateResponse(
        request = request,
        name="write_letter.html",
        context={"request": request}
    )