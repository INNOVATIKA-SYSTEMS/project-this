from fastapi import FastAPI
from server.api.crud_router import router as items_router

app = FastAPI()
app.include_router(items_router)  # Подключаем роутер
