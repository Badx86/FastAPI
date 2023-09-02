from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, users
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

# Инициализация FastAPI-приложения
app = FastAPI()

# Создание всех таблиц в базе данных согласно моделям из модуля `models`
models.Base.metadata.create_all(bind=engine)

# Подключение статических файлов из папки "static"
# Все файлы будут доступны по пути /static/{filename}
app.mount("/static", StaticFiles(directory="static"), name="static")


# Редирект с корневого пути на /todos
@app.get("/")
async def root():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# Включение роутеров из модулей `auth`, `todos` и 'users'
# Теперь все пути, определенные в этих роутерах, будут доступны в приложении
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
