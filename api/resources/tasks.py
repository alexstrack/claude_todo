from flask import current_app, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import sqlite3

from api.schemas.task import TaskSchema, TaskUpdateSchema


blp = Blueprint(
    "Tasks",
    __name__,
    description="Operations on tasks",
    url_prefix="/api"
)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@blp.route("/tasks")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        """Get all tasks"""
        db = get_db()
        tasks = db.execute(
            'SELECT id, description, due_date, status, created_at'
            ' FROM tasks'
            ' ORDER BY created_at DESC'
        ).fetchall()
        
        # Convert Row objects to dicts
        tasks_list = [dict(task) for task in tasks]
        return tasks_list

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        """Create a new task"""
        db = get_db()
        
        try:
            cursor = db.execute(
                'INSERT INTO tasks (description, due_date, status)'
                ' VALUES (?, ?, ?)',
                (task_data['description'], task_data['due_date'], task_data.get('status', False))
            )
            task_id = cursor.lastrowid
            db.commit()
            
            # Fetch the created task
            task = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            return dict(task)
            
        except sqlite3.Error as e:
            db.rollback()
            abort(500, message=str(e))


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        """Get a task by ID"""
        db = get_db()
        task = db.execute(
            'SELECT id, description, due_date, status, created_at'
            ' FROM tasks WHERE id = ?',
            (task_id,)
        ).fetchone()
        
        if task is None:
            abort(404, message="Task not found")
            
        return dict(task)
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        """Update a task"""
        db = get_db()
        
        # Check if task exists
        task = db.execute(
            'SELECT id FROM tasks WHERE id = ?',
            (task_id,)
        ).fetchone()
        
        if task is None:
            abort(404, message="Task not found")
        
        # Build update query based on provided fields
        update_fields = []
        params = []
        
        if 'description' in task_data:
            update_fields.append('description = ?')
            params.append(task_data['description'])
            
        if 'due_date' in task_data:
            update_fields.append('due_date = ?')
            params.append(task_data['due_date'])
            
        if 'status' in task_data:
            update_fields.append('status = ?')
            params.append(task_data['status'])
            
        if not update_fields:
            abort(400, message="No fields to update")
            
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
        params.append(task_id)
        
        try:
            db.execute(query, params)
            db.commit()
            
            # Fetch updated task
            updated_task = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            return dict(updated_task)
            
        except sqlite3.Error as e:
            db.rollback()
            abort(500, message=str(e))
    
    @blp.response(204)
    def delete(self, task_id):
        """Delete a task"""
        db = get_db()
        
        # Check if task exists
        task = db.execute(
            'SELECT id FROM tasks WHERE id = ?',
            (task_id,)
        ).fetchone()
        
        if task is None:
            abort(404, message="Task not found")
            
        try:
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            db.commit()
            return {}
            
        except sqlite3.Error as e:
            db.rollback()
            abort(500, message=str(e))