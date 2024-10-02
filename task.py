from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import task, user
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get('/all_tasks')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(task.Task)).all()
    return tasks

@router.get('/task_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task1 = db.scalar(select(task.Task).where(task.Task.id == task_id))
    if task1 is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task1

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user1 = db.scalar(select(user.User).where(user.User.id == user_id))
    if user1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.execute(insert(task.Task).values(title= create_task.title,
                                   content= create_task.content,
                                   priority= create_task.priority,
                                   user_id = user_id,
                                   slug= slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Succesful'}

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], update_task: UpdateTask, task_id: int):
    task1 = db.scalar(select(task.Task).where(task.Task.id == task_id))
    if task1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no task found")
    db.execute(update(task.Task).where(task.Task.id == task_id).values(title= update_task.title,
                                                       content= update_task.content,
                                                       priority= update_task.priority,
                                                             slug= slugify(update_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task1 = db.scalar(select(task.Task).where(task.Task.id == task_id))
    if task1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no task found")
    db.execute(delete(task.Task).where(task.Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}