from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# Определение модели пользователей
class Users(Base):
    __tablename__ = "users"

    # Определение столбцов для таблицы users
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Определение связи один ко многим с таблицей todos
    todos = relationship("Todos", back_populates="owner")


# Определение модели задач (to-dos)
class Todos(Base):
    __tablename__ = "todos"

    # Определение столбцов для таблицы todos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Определение обратной связи с таблицей users
    owner = relationship("Users", back_populates="todos")
