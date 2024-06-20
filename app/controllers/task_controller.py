from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services import task_service
from app.models.task_model import TaskResponse, TaskCreate, TaskUpdate
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.title, task.description)

@router.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = task_service.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = task_service.update_task(db, task_id, task.title, task.description, task.status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}