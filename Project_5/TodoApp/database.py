from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Создание движка SQLAlchemy
# `check_same_thread`: Отключает проверку того, что тот же поток используется в течение всего процесса
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Конфигурация сессии SQLAlchemy для работы с базой данных
# `autocommit`: автоматическое подтверждение транзакций (отключено)
# `autoflush`: автоматическое сбрасывание буфера сессии (отключено)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для декларативных моделей базы данных
Base = declarative_base()
