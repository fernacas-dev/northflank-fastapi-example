# Task List with FastAPI and React

A Task List (To-Do List) application built with FastAPI in the backend and React in the frontend, using Redis for storage.

## Features

- **Backend (FastAPI)**:
  - RESTful API for task management
  - Redis storage
  - Automatic documentation with Swagger UI

- **Frontend (React)**:
  - Intuitive and responsive user interface
  - State management with React Hooks
  - Modern and accessible design

## Prerequisites

- Python 3.8+
- Node.js 16+
- Redis
- npm or yarn

## Project Setup

### Backend

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configure environment variables (optional, create a `.env` file in the backend folder):
   ```
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

The server will be available at `http://localhost:8000`

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Configure the API URL (optional, modify in `src/App.js`):
   ```javascript
   const API_URL = 'http://localhost:8000';
   ```

3. Run the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## Deployment

### Backend (Northflank)

1. Create a new project in Northflank
2. Add a Redis service
3. Configure environment variables to connect to Redis
4. Deploy the backend code

### Frontend (Vercel)

1. Connect your GitHub repository with Vercel
2. Set the build directory to `frontend`
3. Set the build command: `npm run build`
4. Configure the `REACT_APP_API_URL` environment variable with your deployed API URL

## Project Structure

```
.
├── backend/               # FastAPI server code
│   ├── main.py            # Application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # React application
│   ├── public/            # Static files
│   └── src/               # React source code
└── README.md              # This file
```

## API Endpoints

- `GET /tasks/` - Get all tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## License

This project is licensed under the MIT License.
