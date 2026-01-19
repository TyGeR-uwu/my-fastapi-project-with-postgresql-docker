from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/groups", tags=["Группы"])


@router.post("/create", summary="Создать группу")
def create_group(
    group_name: str = Query(...),
    group_id: int = Query(None),
    db: Session = Depends(get_db)
):
    group_data = schemas.GroupCreate(group_name=group_name, group_id=group_id)
    return crud.create_group(db=db, group=group_data)


@router.get("/info", summary="Получить инфо группы по group_id")
def get_group(group_id: int = Query(...), db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@router.get("/list", summary="Получить список групп")
def get_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)


@router.delete("/delete", summary="Удалить группу по group_id")
def delete_group(group_id: int = Query(...), db: Session = Depends(get_db)):
    success = crud.delete_group(db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted"}