"""
Главный модуль FastAPI приложения.
Создает и настраивает приложение FastAPI.
"""
import sys
sys.path.append('/app')
from fastapi import FastAPI
from .database import engine, Base
from .api.routes import router

# Создаем таблицы в базе данных (в продакшене используйте миграции)
Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI
app = FastAPI(
    title="Student Management API",
    description="API для управления студентами и группами",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(router)

@app.get("/")
def read_root():
    """
    Корневой эндпоинт.
    Возвращает информацию о API.
    """
    return {
        "message": "Добро пожаловать в Student Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """
    Проверка работоспособности API.
    """
    return {"status": "healthy"}