# core/db.py
import reflex as rx
from sqlalchemy import (create_engine, Column, Integer, String, Enum as SQLAlchemyEnum, DateTime, Boolean)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

# Frontend Data Model
class TaskModel(rx.Base):
    id: int
    description: str
    status: str
    due_date: datetime | None = None
    completed: bool

# Backend Database Model
DATABASE_URL = "sqlite:///./mytaskmate.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

Base.metadata.create_all(bind=engine)

# Database Functions
def get_all_tasks_from_db() -> list[Task]:
    with SessionLocal() as db:
        return db.query(Task).order_by(Task.id).all()

def add_task_to_db(description: str, due_date: datetime = None) -> Task:
    with SessionLocal() as db:
        new_task = Task(description=description, due_date=due_date)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

def update_task_status_in_db(task_id: int, status: TaskStatus) -> Task:
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task: raise ValueError(f"Task ID {task_id} not found.")
        task.status = status
        task.completed = (status == TaskStatus.COMPLETED)
        db.commit()
        db.refresh(task)
        return task

def reschedule_task_in_db(task_id: int, new_due_date: datetime) -> Task:
    with SessionLocal() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task: raise ValueError(f"Task ID {task_id} not found.")
        task.due_date = new_due_date
        db.commit()
        db.refresh(task)
        return task