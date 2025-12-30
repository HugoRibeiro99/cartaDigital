from fastapi import FastAPI

app = FastAPI()
# INICIAR APP: uvicorn main:app --reload

from auth_routes import auth_router

app.include_router(auth_router)