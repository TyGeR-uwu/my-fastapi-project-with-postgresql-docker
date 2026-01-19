from sqlalchemy.orm import Session
from . import models, schemas


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.group_id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def delete_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.group_id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False


def add_student_to_group(db: Session, student_group: schemas.StudentGroupCreate):
    db_sg = models.StudentGroup(**student_group.dict())
    db.add(db_sg)
    db.commit()
    db.refresh(db_sg)
    return db_sg


def remove_student_from_group(db: Session, student_id: int, group_id: int):
    db_sg = db.query(models.StudentGroup).filter(
        models.StudentGroup.student_id == student_id,
        models.StudentGroup.group_id == group_id
    ).first()
    if db_sg:
        db.delete(db_sg)
        db.commit()
        return True
    return False


def get_students_in_group(db: Session, group_id: int):
    return db.query(models.Student).join(models.StudentGroup).filter(
        models.StudentGroup.group_id == group_id
    ).all()


def change_student_group(db: Session, student_id: int, old_group_id: int, new_group_id: int):
    db_sg = db.query(models.StudentGroup).filter(
        models.StudentGroup.student_id == student_id,
        models.StudentGroup.group_id == old_group_id
    ).first()
    if db_sg:
        db_sg.group_id = new_group_id
        db.commit()
        db.refresh(db_sg)
        return db_sg
    return None