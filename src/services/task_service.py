from sqlalchemy.orm import Session
from ..db.models import Task, User, TaskStatus
from fastapi import HTTPException

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    async def create_task(self, username: str, task_description: str) -> Task:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        task = Task(
            assigned_user_id=user.user_id,
            task_description=task_description,
            status=TaskStatus.PENDING
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    async def get_user_tasks(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.assigned_user_id == user_id).all()

    async def update_task_status(self, task_id: int, user_id: int, new_status: TaskStatus) -> Task:
        task = self.db.query(Task).filter(
            Task.task_id == task_id,
            Task.assigned_user_id == user_id
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or not assigned to you")

        task.status = new_status
        self.db.commit()
        self.db.refresh(task)
        return task