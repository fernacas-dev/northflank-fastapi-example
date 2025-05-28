import React, { useState, useEffect } from 'react';
import './App.css';

// API URL from environment variables
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/tasks/`);
      if (!response.ok) throw new Error('Failed to load tasks');
      const data = await response.json();
      setTasks(Array.isArray(data) ? data : []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await fetch(`${API_URL}/tasks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newTaskTitle,
          completed: false,
        }),
      });

      if (!response.ok) throw new Error('Failed to add task');
      
      setNewTaskTitle('');
      await fetchTasks();
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    }
  };

  const toggleTask = async (taskId, currentStatus) => {
    try {
      const taskToUpdate = tasks.find(t => t.id === taskId);
      if (!taskToUpdate) return;
      
      const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: taskToUpdate.title,
          completed: !currentStatus,
        }),
      });

      if (!response.ok) throw new Error('Failed to update task');
      
      await fetchTasks();
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    }
  };

  const deleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    
    try {
      const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete task');
      
      await fetchTasks();
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Task List</h1>
      </header>
      
      <main>
        <form onSubmit={addTask} className="task-form">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="New task..."
            className="task-input"
            maxLength={100}
          />
          <button type="submit" className="add-button" disabled={!newTaskTitle.trim()}>
            Add Task
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <p className="loading">Loading tasks...</p>
        ) : (
          <ul className="task-list">
            {tasks.length > 0 ? (
              tasks.map((task) => (
                <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <input
                    type="checkbox"
                    checked={task.completed || false}
                    onChange={() => toggleTask(task.id, task.completed)}
                    className="task-checkbox"
                    aria-label={task.completed ? 'Mark as pending' : 'Mark as complete'}
                  />
                  <span className="task-title">{task.title}</span>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="delete-button"
                    aria-label="Delete task"
                  >
                    🗑️
                  </button>
                </li>
              ))
            ) : (
              <li className="no-tasks">No tasks yet. Add a new task to get started!</li>
            )}
          </ul>
        )}
      </main>
      
      <footer>
        <p>Total tasks: {tasks.length} | Completed: {tasks.filter(t => t.completed).length}</p>
      </footer>
    </div>
  );
}

export default App;
