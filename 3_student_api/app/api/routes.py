"""
Модуль с API эндпоинтами.
Определяет все маршруты для работы со студентами и группами.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

# Создаем роутеры
router = APIRouter()

# Эндпоинты для студентов
@router.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Создает нового студента.
    """
    return crud.create_student(db=db, student=student)

@router.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Получает информацию о студенте по его ID.
    """
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получает список всех студентов.
    """
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о студенте.
    """
    db_student = crud.update_student(db, student_id=student_id, student_update=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Удаляет студента.
    """
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return None

# Эндпоинты для групп
@router.post("/groups/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """
    Создает новую группу.
    """
    return crud.create_group(db=db, group=group)

@router.get("/groups/{group_id}", response_model=schemas.GroupWithStudents)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """
    Получает информацию о группе по ее ID.
    """
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@router.get("/groups/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получает список всех групп.
    """
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@router.put("/groups/{group_id}", response_model=schemas.Group)
def update_group(group_id: int, group: schemas.GroupUpdate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о группе.
    """
    db_group = crud.update_group(db, group_id=group_id, group_update=group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """
    Удаляет группу.
    """
    success = crud.delete_group(db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return None

# Эндпоинты для связи студент-группа
@router.post("/groups/{group_id}/students/{student_id}", response_model=schemas.Student)
def add_student_to_group_endpoint(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """
    Добавляет студента в группу.
    """
    result = crud.add_student_to_group(db, student_id=student_id, group_id=group_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Студент или группа не найдены")
    return result

@router.delete("/groups/{group_id}/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_student_from_group_endpoint(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """
    Удаляет студента из группы.
    """
    result = crud.remove_student_from_group(db, student_id=student_id, group_id=group_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Студент или группа не найдены")
    return None

@router.get("/groups/{group_id}/students/", response_model=List[schemas.Student])
def get_students_in_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    """
    Получает всех студентов в группе.
    """
    students = crud.get_students_in_group(db, group_id=group_id)
    return students

@router.post("/students/{student_id}/transfer/")
def transfer_student_endpoint(
    student_id: int, 
    from_group_id: int, 
    to_group_id: int, 
    db: Session = Depends(get_db)
):
    """
    Переводит студента из группы A в группу B.
    """
    result = crud.transfer_student(db, student_id=student_id, from_group_id=from_group_id, to_group_id=to_group_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Студент или группы не найдены")
    return {"message": "Студент успешно переведен", "student": result}