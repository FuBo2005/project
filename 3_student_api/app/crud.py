"""
Модуль с функциями для работы с базой данных (CRUD операции).
"""

from sqlalchemy.orm import Session
from . import models, schemas

# Операции для студентов
def create_student(db: Session, student: schemas.StudentCreate):
    """
    Создает нового студента в базе данных.
    """
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    """
    Получает студента по ID.
    """
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список студентов с пагинацией.
    """
    return db.query(models.Student).offset(skip).limit(limit).all()

def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate):
    """
    Обновляет информацию о студенте.
    """
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    """
    Удаляет студента по ID.
    """
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

# Операции для групп
def create_group(db: Session, group: schemas.GroupCreate):
    """
    Создает новую группу.
    """
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: int):
    """
    Получает группу по ID.
    """
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список групп.
    """
    return db.query(models.Group).offset(skip).limit(limit).all()

def update_group(db: Session, group_id: int, group_update: schemas.GroupUpdate):
    """
    Обновляет информацию о группе.
    """
    db_group = get_group(db, group_id)
    if db_group:
        update_data = group_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_group, key, value)
        db.commit()
        db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    """
    Удаляет группу по ID.
    """
    db_group = get_group(db, group_id)
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

# Операции для связи студент-группа
def add_student_to_group(db: Session, student_id: int, group_id: int):
    """
    Добавляет студента в группу.
    """
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    
    if student and group:
        if group not in student.groups:
            student.groups.append(group)
            db.commit()
        return student
    return None

def remove_student_from_group(db: Session, student_id: int, group_id: int):
    """
    Удаляет студента из группы.
    """
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    
    if student and group:
        if group in student.groups:
            student.groups.remove(group)
            db.commit()
        return student
    return None

def get_students_in_group(db: Session, group_id: int):
    """
    Получает всех студентов в группе.
    """
    group = get_group(db, group_id)
    if group:
        return group.students
    return []

def transfer_student(db: Session, student_id: int, from_group_id: int, to_group_id: int):
    """
    Переводит студента из одной группы в другую.
    """
    # Удаляем студента из исходной группы
    remove_student_from_group(db, student_id, from_group_id)
    
    # Добавляем в новую группу
    result = add_student_to_group(db, student_id, to_group_id)
    return result