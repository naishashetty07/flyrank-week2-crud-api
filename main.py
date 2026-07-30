from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import (
    create_database,
    get_all_tasks,
    get_task_by_id,
    create_task_db,
    update_task_db,
    delete_task_db,
)

app = FastAPI()

create_database()


class Task(BaseModel):
    title: str
    done: bool


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/health",
            "/tasks",
            "/tasks/{task_id}"
        ]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    return create_task_db(task.title, task.done)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    task = update_task_db(
        task_id,
        updated_task.title,
        updated_task.done
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    success = delete_task_db(task_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return