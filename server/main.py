from fastapi import FastAPI
from server.api.crud_router import router as items_router

app = FastAPI()

# Подключаем роутер
app.include_router(items_router)  

# Главная страница
app.get("/")
async def root():
    return {"message":"main page"}

# О проекте
app.get("/about")
async def about():
    return {"message":"about project"}

# Данные
app.get("/date")
async def date():
    return {"message":"date info"}

# Админка
app.get("/admin")
async def admin():
    return {"message":"admin info"}