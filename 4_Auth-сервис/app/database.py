from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем URL базы данных из переменных окружения
# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок SQLAlchemy
# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
# Base class for models
Base = declarative_base()

# Зависимость для получения сессии базы данных
# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()