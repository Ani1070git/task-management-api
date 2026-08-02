from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Task, User
from fastapi.security import OAuth2PasswordBearer
from auth import hash_password, verify_password, create_access_token, verify_token
from ai import extract_task_from_message

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TaskInput(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class UserInput(BaseModel):
    username: str
    password: str

class AITaskInput(BaseModel):
    message: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

@app.get("/tasks")
def get_tasks(db = Depends(get_db),current_user: str = Depends(get_current_user)):
    return db.query(Task).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db = Depends(get_db), current_user: str = Depends(get_current_user)):
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code = 404, detail ="Task not found")
        return task

@app.put("/tasks/{task_id}")
def update_task(task: TaskUpdate, task_id: int, db = Depends(get_db),current_user: str = Depends(get_current_user)):
    task_db = db.query(Task).filter(Task.id == task_id).first()

    if task_db is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    if task.title is not None:
        task_db.title = task.title
    if task.done is not None:
        task_db.done = task.done
    
    db.commit()
    db.refresh(task_db)
    return task_db

@app.post("/tasks")
def new_tasks(task: TaskInput, db = Depends(get_db),current_user: str = Depends(get_current_user)):
    new_task = Task(title=task.title, done=task.done)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,db = Depends(get_db),current_user: str = Depends(get_current_user)):
    del_task = db.query(Task).filter(Task.id == task_id).first()

    if del_task is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(del_task)
    db.commit()
    
    return {"message" :f"task {task_id} deleted successfully"}

@app.post("/register")
def register(user: UserInput, db = Depends(get_db)):
    exsiting_user = db.query(User).filter(User.username == user.username).first()
    if exsiting_user:
        raise HTTPException(status_code=400, detail="username already exsists")
    hashed = hash_password(user.password)
    new_user = User(username = user.username, hashed_password = hashed)
    db.add(new_user)
    db.commit()
    return {"message": "user name registered sucessfully"}

@app.post("/login")
def login(user: UserInput, db = Depends(get_db)):
    user_exisiting = db.query(User).filter(User.username == user.username).first()
    if user_exisiting is None:
        raise HTTPException(status_code=401, detail="Invalid credientials")
    is_valid = verify_password(user.password, user_exisiting.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="invlaid credential")
    access_token = create_access_token({"sub": str(user_exisiting.id)})

    return access_token
    

@app.post("/tasks/ai")
def create_task_from_message(task: AITaskInput, db = Depends(get_db), current_user: str = Depends(get_current_user)):
    task_title = extract_task_from_message(task.message)
    new_task = Task(title= task_title, done= False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
