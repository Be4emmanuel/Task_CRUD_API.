from fastapi import FastAPI, status
from models import TaskCreate, TaskResponse

app = FastAPI(title="Task CRUD API")

tasks = []
next_task_id = 1


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