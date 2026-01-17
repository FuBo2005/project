from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from .database import engine
from . import models
from .routes import router
import logging
import time

# Создаем таблицы в базе данных (в продакшене используйте миграции!)
# Create database tables (use migrations in production!)
models.Base.metadata.create_all(bind=engine)

# Настройка логгирования
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI"""
    # Действия при запуске приложения
    # Actions on application startup
    logger.info("Auth Service starting up...")
    yield
    # Действия при остановке приложения
    # Actions on application shutdown
    logger.info("Auth Service shutting down...")

# Создаем приложение FastAPI
# Create FastAPI application
app = FastAPI(
    title="Auth Service",
    description="Сервис аутентификации и авторизации",
    version="1.0.0",
    lifespan=lifespan
)

# Добавляем middleware для отладки запросов
# Add middleware for request debugging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware для логирования запросов"""
    # Middleware for request logging
    start_time = time.time()
    
    # Логируем входящий запрос
    # Log incoming request
    logger.info(f"Входящий запрос: {request.method} {request.url.path}")
    
    # Продолжаем обработку запроса
    # Continue request processing
    response = await call_next(request)
    
    # Вычисляем время обработки
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Логируем результат
    # Log result
    logger.info(f"Ответ: {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

# Подключаем маршруты
# Include routes
app.include_router(router)

# Корневой эндпоинт
# Root endpoint
@app.get("/")
def read_root():
    """Корневой эндпоинт API"""
    # Root API endpoint
    return {
        "message": "Auth Service API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Эндпоинт для проверки здоровья
# Health check endpoint
@app.get("/health")
def health_check():
    """Проверка здоровья сервиса"""
    # Service health check
    return {"status": "healthy", "service": "auth-service"}

# Эндпоинт для отладки (если нужно)
# Debug endpoint (if needed)
@app.get("/debug")
def debug_info():
    """Информация для отладки"""
    # Debug information
    return {
        "service": "Auth Service",
        "version": "1.0.0",
        "database": "connected" if engine else "disconnected"
    }