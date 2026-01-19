from pydantic import BaseModel
from typing import Optional


class StudentBase(BaseModel):
    fio: str
    email: str


class StudentCreate(StudentBase):
    student_id: Optional[int] = None


class Student(StudentBase):
    student_id: int

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    group_name: str


class GroupCreate(GroupBase):
    group_id: Optional[int] = None


class Group(GroupBase):
    group_id: int

    class Config:
        from_attributes = True


class StudentGroupBase(BaseModel):
    student_id: int
    group_id: int


class StudentGroupCreate(StudentGroupBase):
    pass


class StudentGroup(StudentGroupBase):
    pass

    class Config:
        from_attributes = True