from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos
from starlette.staticfiles import StaticFiles


# Инициализация FastAPI-приложения
app = FastAPI()

# Создание всех таблиц в базе данных согласно моделям из модуля `models`
models.Base.metadata.create_all(bind=engine)

# Подключение статических файлов из папки "static"
# Все файлы будут доступны по пути /static/{filename}
app.mount("/static", StaticFiles(directory="static"), name="static")

# Включение роутеров из модулей `auth` и `todos`
# Теперь все пути, определенные в этих роутерах, будут доступны в приложении
app.include_router(auth.router)
app.include_router(todos.router)
