from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Task, User
from ..services.task_service import TaskService
import os
from jose import JWTError, jwt

app = FastAPI(title="Task Management API")
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/tasks/{user_id}")
async def get_user_tasks(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    task_service = TaskService(db)
    tasks = await task_service.get_user_tasks(user_id)
    return {"tasks": [{"id": t.task_id, "description": t.task_description, "status": t.status.value} for t in tasks]}

@app.get("/tasks/status/{status}")
async def get_tasks_by_status(
    status: str,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    tasks = db.query(Task).filter(Task.status == status).all()
    return {"tasks": [{"id": t.task_id, "description": t.task_description, "assigned_to": t.assigned_user_id} for t in tasks]}