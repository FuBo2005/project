"""
Модуль с Pydantic схемами.
Используется для валидации входных и выходных данных API.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Схемы для студентов
class StudentBase(BaseModel):
    """Базовая схема студента."""
    full_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    """Схема для создания студента."""
    pass

class StudentUpdate(BaseModel):
    """Схема для обновления студента."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class Student(StudentBase):
    """Схема для отображения студента."""
    id: int
    
    class Config:
        from_attributes = True

# Схемы для групп
class GroupBase(BaseModel):
    """Базовая схема группы."""
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    """Схема для создания группы."""
    pass

class GroupUpdate(BaseModel):
    """Схема для обновления группы."""
    name: Optional[str] = None
    description: Optional[str] = None

class Group(GroupBase):
    """Схема для отображения группы."""
    id: int
    students: List[Student] = []
    
    class Config:
        from_attributes = True

class GroupWithStudents(Group):
    """Схема группы с информацией о студентах."""
    students: List[Student]