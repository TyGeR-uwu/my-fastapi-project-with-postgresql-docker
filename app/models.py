from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    fio = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    groups = relationship("StudentGroup", back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint('group_id > 0', name='check_group_id_positive'),
    )

    students = relationship("StudentGroup", back_populates="group")


class StudentGroup(Base):
    __tablename__ = "student_group"

    student_id = Column(Integer, ForeignKey("students.student_id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)

    student = relationship("Student", back_populates="groups")
    group = relationship("Group", back_populates="students")