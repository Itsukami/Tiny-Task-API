from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import sqlite3
from typing import List, Optional

from app.db import init_db, get_db_connection
from app.models import TaskCreate, TaskUpdate, TaskResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Tiny Task API", lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msg = f"Validation error: {errors[0]['loc'][-1]} - {errors[0]['msg']}"
    return JSONResponse(
        status_code=400,
        content={"error": error_msg},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,))
        db.commit()
        task_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    done: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: sqlite3.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()
    
    query = "SELECT * FROM tasks"
    params = []
    
    if done is not None:
        query += " WHERE done = ?"
        params.append(1 if done else 0)
    
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return dict(row)

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: sqlite3.Connection = Depends(get_db_connection)
):
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    
    if not update_data:
        return dict(existing_task)
    
    set_clauses = []
    values = []
    
    for key, value in update_data.items():
        set_clauses.append(f"{key} = ?")
        if isinstance(value, bool):
            values.append(1 if value else 0)
        else:
            values.append(value)
            
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"
    
    cursor.execute(query, values)
    db.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    return dict(row)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return None