from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import redis
import json
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS from environment variables
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001')
allow_origins = cors_origins.split(',') if cors_origins != '*' else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=os.getenv('CORS_ALLOW_CREDENTIALS', 'true').lower() == 'true',
    allow_methods=os.getenv('CORS_ALLOW_METHODS', '*').split(','),
    allow_headers=os.getenv('CORS_ALLOW_HEADERS', '*').split(','),
)

# Redis configuration using environment variables
redis_password = os.getenv('REDIS_PASSWORD')
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=redis_password if redis_password else None,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_keepalive=True
)

class Task(BaseModel):
    id: str = None
    title: str
    completed: bool = False

# Generate unique ID
def generate_id():
    return str(uuid.uuid4())

@app.post("/tasks/")
async def create_task(task: Task):
    task_id = generate_id()
    task_data = task.dict()
    task_data["id"] = task_id
    redis_client.set(f"task:{task_id}", json.dumps(task_data))
    return task_data

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task_data = redis_client.get(f"task:{task_id}")
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return json.loads(task_data)

@app.get("/tasks/")
async def get_tasks():
    keys = redis_client.keys("task:*")
    tasks = []
    for key in keys:
        task_data = redis_client.get(key)
        if task_data:
            tasks.append(json.loads(task_data))
    return tasks

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    if not redis_client.exists(f"task:{task_id}"):
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict()
    task_data["id"] = task_id
    redis_client.set(f"task:{task_id}", json.dumps(task_data))
    return task_data

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if not redis_client.exists(f"task:{task_id}"):
        raise HTTPException(status_code=404, detail="Task not found")
    redis_client.delete(f"task:{task_id}")
    return {"message": "Task deleted successfully"}