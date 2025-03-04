from flask import current_app, g, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import sqlite3
import json
import traceback

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
        try:
            db = get_db()
            tasks = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks'
                ' ORDER BY created_at DESC'
            ).fetchall()
            
            # Convert Row objects to dicts manually to avoid serialization issues
            task_list = []
            for task in tasks:
                task_dict = {
                    'id': task['id'],
                    'description': task['description'],
                    'due_date': task['due_date'],
                    'status': bool(task['status']),
                }
                if task['created_at']:
                    task_dict['created_at'] = task['created_at']
                task_list.append(task_dict)
                
            return task_list
        except Exception as e:
            current_app.logger.error(f"Error getting tasks: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=str(e))

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        """Create a new task"""
        db = get_db()
        
        try:
            # Ensure data is properly formatted
            description = task_data['description']
            due_date = task_data['due_date']
            status = task_data.get('status', False)
            
            # Insert the task
            cursor = db.execute(
                'INSERT INTO tasks (description, due_date, status)'
                ' VALUES (?, ?, ?)',
                (description, due_date, 1 if status else 0)
            )
            task_id = cursor.lastrowid
            db.commit()
            
            # Fetch the created task
            task = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            # Convert to dict for consistent response
            task_dict = {
                'id': task['id'],
                'description': task['description'],
                'due_date': task['due_date'],
                'status': bool(task['status']),
            }
            if task['created_at']:
                task_dict['created_at'] = task['created_at']
                
            return task_dict
            
        except Exception as e:
            current_app.logger.error(f"Error creating task: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            db.rollback()
            abort(500, message=str(e))


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        """Get a task by ID"""
        try:
            db = get_db()
            task = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            if task is None:
                abort(404, message="Task not found")
            
            # Convert to dict for consistent response
            task_dict = {
                'id': task['id'],
                'description': task['description'],
                'due_date': task['due_date'],
                'status': bool(task['status']),
            }
            if task['created_at']:
                task_dict['created_at'] = task['created_at']
                
            return task_dict
                
        except Exception as e:
            current_app.logger.error(f"Error getting task {task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=str(e))
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        """Update a task"""
        db = get_db()
        
        try:
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
            
            if 'description' in task_data and task_data['description'] is not None:
                update_fields.append('description = ?')
                params.append(task_data['description'])
                
            if 'due_date' in task_data and task_data['due_date'] is not None:
                update_fields.append('due_date = ?')
                params.append(task_data['due_date'])
                
            if 'status' in task_data:
                update_fields.append('status = ?')
                params.append(1 if task_data['status'] else 0)  # Convert to 0 or 1 for SQLite
                
            if not update_fields:
                abort(400, message="No fields to update")
                
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            params.append(task_id)
            
            db.execute(query, params)
            db.commit()
            
            # Fetch updated task
            updated_task = db.execute(
                'SELECT id, description, due_date, status, created_at'
                ' FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            # Convert to dict for consistent response
            task_dict = {
                'id': updated_task['id'],
                'description': updated_task['description'],
                'due_date': updated_task['due_date'],
                'status': bool(updated_task['status']),
            }
            if updated_task['created_at']:
                task_dict['created_at'] = updated_task['created_at']
                
            return task_dict
            
        except Exception as e:
            current_app.logger.error(f"Error updating task {task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            db.rollback()
            abort(500, message=str(e))
    
    @blp.response(204)
    def delete(self, task_id):
        """Delete a task"""
        db = get_db()
        
        try:
            # Check if task exists
            task = db.execute(
                'SELECT id FROM tasks WHERE id = ?',
                (task_id,)
            ).fetchone()
            
            if task is None:
                abort(404, message="Task not found")
                
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            db.commit()
            return {}
                
        except Exception as e:
            current_app.logger.error(f"Error deleting task {task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            db.rollback()
            abort(500, message=str(e))