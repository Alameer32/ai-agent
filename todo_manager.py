import json
import os
from datetime import datetime

TODOS_FILE = "todos.json"

def load_todos():
    """Load todos from JSON file"""
    if not os.path.exists(TODOS_FILE):
        return []
    with open(TODOS_FILE, "r") as f:
        return json.load(f)

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def create_task(title, description=""):
    """Create a new task"""
    todos = load_todos()
    task_id = len(todos) + 1
    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    todos.append(new_task)
    save_todos(todos)
    return f"✅ Task created: '{title}'"

def view_all_tasks():
    """View all tasks"""
    todos = load_todos()
    if not todos:
        return "📝 No tasks found. Create your first task!"
    
    result = "📋 Your Tasks:\n"
    for task in todos:
        status = "✅" if task["completed"] else "⏳"
        result += f"{status} [{task['id']}] {task['title']}"
        if task["description"]:
            result += f" - {task['description']}"
        result += "\n"
    
    return result.strip()

def mark_task_done(task_id):
    """Mark a task as completed"""
    todos = load_todos()
    for task in todos:
        if task["id"] == task_id:
            if task["completed"]:
                return f"Task '{task['title']}' is already completed!"
            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat()
            save_todos(todos)
            return f"🎉 Task completed: '{task['title']}'"
    return f"❌ Task with ID {task_id} not found."

def delete_task(task_id):
    """Delete a task"""
    todos = load_todos()
    for i, task in enumerate(todos):
        if task["id"] == task_id:
            deleted_task = todos.pop(i)
            save_todos(todos)
            return f"🗑️ Task deleted: '{deleted_task['title']}'"
    return f"❌ Task with ID {task_id} not found."

def get_pending_tasks():
    """Get count of pending tasks"""
    todos = load_todos()
    pending = [task for task in todos if not task["completed"]]
    completed = [task for task in todos if task["completed"]]
    return {
        "pending": len(pending),
        "completed": len(completed),
        "total": len(todos)
    }

def view_pending_tasks():
    """View only pending tasks"""
    todos = load_todos()
    pending = [task for task in todos if not task["completed"]]
    
    if not pending:
        return "🎉 No pending tasks! You're all caught up!"
    
    result = "⏳ Pending Tasks:\n"
    for task in pending:
        result += f"[{task['id']}] {task['title']}"
        if task["description"]:
            result += f" - {task['description']}"
        result += "\n"
    
    return result.strip()

def view_completed_tasks():
    """View only completed tasks"""
    todos = load_todos()
    completed = [task for task in todos if task["completed"]]
    
    if not completed:
        return "📝 No completed tasks yet."
    
    result = "✅ Completed Tasks:\n"
    for task in completed:
        result += f"[{task['id']}] {task['title']}"
        if task["description"]:
            result += f" - {task['description']}"
        result += "\n"
    
    return result.strip()