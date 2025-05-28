from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import redis
import json
import uuid
import os
from datetime import datetime
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

# Redis connection configuration
redis_config = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'password': os.getenv('REDIS_PASSWORD'),
    'decode_responses': True,
    'socket_timeout': 5,
    'socket_connect_timeout': 5,
    'retry_on_timeout': True,
    'max_connections': 20,
    'health_check_interval': 30,
    'ssl': True,  # Enable SSL/TLS
    'ssl_cert_reqs': None,  # Don't require client certificate
    'ssl_ca_certs': None,  # Use system's default CA certificates
}

# Remove None values from config
redis_config = {k: v for k, v in redis_config.items() if v is not None}

# Create Redis connection pool
redis_pool = redis.ConnectionPool(**redis_config)
redis_client = redis.Redis(connection_pool=redis_pool)

def get_redis_connection():
    """Get a Redis connection from the pool with error handling"""
    try:
        # Test the connection
        redis_client.ping()
        return redis_client
    except redis.RedisError as e:
        print(f"Redis connection error: {e}")
        # Attempt to reconnect
        redis_client.connection_pool.disconnect()
        return redis.Redis(connection_pool=redis_pool)

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
    redis_conn = get_redis_connection()
    redis_conn.set(f"task:{task_id}", json.dumps(task_data))
    return task_data

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    redis_conn = get_redis_connection()
    task_data = redis_conn.get(f"task:{task_id}")
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return json.loads(task_data)

@app.get("/tasks/")
async def get_tasks():
    redis_conn = get_redis_connection()
    try:
        keys = redis_conn.keys("task:*")
        tasks = []
        for key in keys:
            task_data = redis_conn.get(key)
            if task_data:
                tasks.append(json.loads(task_data))
        return tasks
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    redis_conn = get_redis_connection()
    if not redis_conn.exists(f"task:{task_id}"):
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict()
    task_data["id"] = task_id
    redis_conn.set(f"task:{task_id}", json.dumps(task_data))
    return task_data

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    redis_conn = get_redis_connection()
    if not redis_conn.exists(f"task:{task_id}"):
        raise HTTPException(status_code=404, detail="Task not found")
    redis_conn.delete(f"task:{task_id}")
    return {"message": "Task deleted successfully"}

@app.get("/health", status_code=200)
async def health_check():
    """
    Health check endpoint that verifies the API and Redis connection status.
    Returns 200 if both API and Redis are working, 500 otherwise.
    """
    try:
        # Test Redis connection
        redis_conn = get_redis_connection()
        redis_conn.ping()
        return {
            "status": "healthy",
            "api": {
                "status": "up"
            },
            "redis": {
                "status": "connected",
                "host": redis_config.get('host'),
                "port": redis_config.get('port')
            },
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "unhealthy",
                "error": f"Redis connection failed: {str(e)}",
                "timestamp": str(datetime.utcnow())
            }
        )
    return {"message": "Task deleted successfully"}