from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/students", tags=["Студенты"])


@router.post("/create", summary="Создать студента")
def create_student(
    fio: str = Query(...),
    email: str = Query(...),
    student_id: int = Query(None),
    db: Session = Depends(get_db)
):
    student_data = schemas.StudentCreate(fio=fio, email=email, student_id=student_id)
    return crud.create_student(db=db, student=student_data)


@router.get("/info", summary="Получить инфо студента по student_id")
def get_student(student_id: int = Query(...), db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.get("/list", summary="Получить список студентов")
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@router.delete("/delete", summary="Удалить студента по student_id")
def delete_student(student_id: int = Query(...), db: Session = Depends(get_db)):
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}


@router.post("/set_group", summary="Добавить студента в группу")
def set_student_group(
    student_id: int = Query(...),
    group_id: int = Query(...),
    db: Session = Depends(get_db)
):
    sg_data = schemas.StudentGroupCreate(student_id=student_id, group_id=group_id)
    return crud.add_student_to_group(db=db, student_group=sg_data)


@router.delete("/remove_group", summary="Удалить студента из группы")
def remove_student_group(
    student_id: int = Query(...),
    group_id: int = Query(...),
    db: Session = Depends(get_db)
):
    success = crud.remove_student_from_group(db, student_id=student_id, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not in group")
    return {"message": "Student removed from group"}


@router.get("/in_group", summary="Получить всех студентов в группе")
def get_students_in_group(group_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_students_in_group(db, group_id=group_id)


@router.put("/change_group", summary="Перевести студента из группы A в группу B")
def change_student_group(
    student_id: int = Query(...),
    group_id_A: int = Query(...),
    group_id_B: int = Query(...),
    db: Session = Depends(get_db)
):
    result = crud.change_student_group(db, student_id=student_id, old_group_id=group_id_A, new_group_id=group_id_B)
    if result is None:
        raise HTTPException(status_code=404, detail="Student not in specified group")
    return result