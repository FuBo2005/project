from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Проверяет длину пароля"""
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if len(v) > 100:
            raise ValueError('Пароль не должен превышать 100 символов')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Проверяет длину пароля для входа"""
        if len(v) > 100:
            raise ValueError('Пароль не должен превышать 100 символов')
        return v

class TokenRefresh(BaseModel):
    refresh_token: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет длину пароля при обновлении"""
        if v is None:
            return v
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if len(v) > 100:
            raise ValueError('Пароль не должен превышать 100 символов')
        return v

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginHistoryResponse(BaseModel):
    id: int
    user_agent: Optional[str]
    login_time: datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str