import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Настройка маршрутизатора, установка префиксов и тегов для маршрутов
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)
# Инициализация таблиц базы данных
models.Base.metadata.create_all(bind=engine)
# Инициализация системы шаблонов Jinja2
templates = Jinja2Templates(directory="templates")


def get_db():
    """
    Зависимость для получения новой сессии SQLAlchemy SessionLocal.
    Эта сессия будет переиспользована в течение запроса и закрыта после его выполнения.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    """
    Маршрут для чтения всех задач текущего авторизованного пользователя.

    :param request: Объект запроса для получения пользовательской сессии.
    :param db: Сессия SQLAlchemy.
    :return: Отрендеренный шаблон Jinja2.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    """
    Маршрут для добавления новой задачи. Перенаправляет на страницу авторизации, если пользователь не авторизован.

    :param request: Объект запроса для получения пользовательской сессии.
    :return: Отрендеренный шаблон Jinja2 для добавления новой задачи.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    """
    Маршрут для создания новой задачи. Перенаправляет на страницу авторизации, если пользователь не авторизован.

    :param request: Объект запроса для получения пользовательской сессии.
    :param title: Заголовок задачи.
    :param description: Описание задачи.
    :param priority: Приоритет задачи.
    :param db: Сессия SQLAlchemy.
    :return: Перенаправление на страницу со всеми задачами.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Маршрут для редактирования задачи по её идентификатору.

    :param request: Объект запроса для получения пользовательской сессии.
    :param todo_id: Идентификатор задачи.
    :param db: Сессия SQLAlchemy.
    :return: Отрендеренный шаблон для редактирования задачи.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
                           description: str = Form(...), priority: int = Form(...),
                           db: Session = Depends(get_db)):
    """
    Маршрут для сохранения отредактированной задачи.

    :param request: Объект запроса для получения пользовательской сессии.
    :param todo_id: Идентификатор задачи.
    :param title: Новый заголовок задачи.
    :param description: Новое описание задачи.
    :param priority: Новый приоритет задачи.
    :param db: Сессия SQLAlchemy.
    :return: Перенаправление на страницу со всеми задачами.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Маршрут для удаления задачи по её идентификатору.

    :param request: Объект запроса для получения пользовательской сессии.
    :param todo_id: Идентификатор задачи.
    :param db: Сессия SQLAlchemy.
    :return: Перенаправление на страницу со всеми задачами.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Маршрут для изменения статуса задачи (завершена/не завершена).

    :param request: Объект запроса для получения пользовательской сессии.
    :param todo_id: Идентификатор задачи.
    :param db: Сессия SQLAlchemy.
    :return: Перенаправление на страницу со всеми задачами.
    """
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    todo.complete = not todo.complete

    db.add(todo)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
