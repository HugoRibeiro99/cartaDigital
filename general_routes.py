from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

general_router = APIRouter(prefix="/", tags=["/"])


@general_router("/write_letter")
async def write_letter():
    return