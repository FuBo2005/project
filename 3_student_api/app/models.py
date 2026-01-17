"""
Модуль с моделями базы данных.
Определяет таблицы студентов и групп.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Таблица для связи многие-ко-многим между студентами и группами
student_group_association = Table(
    'student_group',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Student(Base):
    """
    Модель студента.
    Хранит информацию о студентах.
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    
    # Связь с группами
    groups = relationship("Group", secondary=student_group_association, back_populates="students")

class Group(Base):
    """
    Модель группы.
    Хранит информацию о группах студентов.
    """
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    # Связь со студентами
    students = relationship("Student", secondary=student_group_association, back_populates="groups")