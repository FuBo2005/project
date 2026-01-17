from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# Модель пользователя
# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Связь с историей входов
    # Relationship with login history
    login_history = relationship("LoginHistory", back_populates="user")

# Модель истории входов
# Login history model
class LoginHistory(Base):
    __tablename__ = "login_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_agent = Column(Text)
    login_time = Column(DateTime, default=func.now())
    
    # Связь с пользователем
    # Relationship with user
    user = relationship("User", back_populates="login_history")