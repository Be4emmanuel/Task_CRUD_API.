from fastapi import FastAPI, HTTPException, status
from models import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(title="Task CRUD API")

tasks = []
next_task_id = 1

def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

@app.get("/health")
def health_check():
    return {"status": "API is healthy"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
    global next_task_id

    new_task = task.model_dump()

    new_task["id"] = next_task_id

    tasks.append(new_task)

    next_task_id += 1

    return new_task

@app.get("/tasks", 
         response_model=list[TaskResponse],
         summary="Get all tasks",
         description="Retrieve a list of all tasks in the system"
)
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}",
         response_model=TaskResponse,
         summary="Get a task by ID",
         description="Retrieve a specific task by its ID"
)
def get_task(task_id: int):
    return find_task(task_id)

@app.put("/tasks/{task_id}", response_model=TaskResponse)

def update_task(task_id: int, task_update: TaskUpdate):
    task = find_task(task_id)

    update_data = task_update.model_dump(exclude_unset=True)
    task.update(update_data)

    return task

@app.delete("/tasks/{task_id}",
            status_code=status.HTTP_200_OK,
            summary="Delete a task by ID"
)
def delete_task(task_id: int):
    index = find_task_index(task_id)
    tasks.pop(index)
    return {"message": "Task deleted successfully"}

def find_task_index(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            return index

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )