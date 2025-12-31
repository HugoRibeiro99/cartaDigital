from fastapi import FastAPI
from auth_routes import auth_router
from general_routes import general_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# INICIAR APP: uvicorn main:app --reload

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(general_router)
