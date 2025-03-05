from flask import current_app, g, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import sqlite3
import traceback

from api.schemas.task import TaskSchema, TaskUpdateSchema


blp = Blueprint(
    "Tasks",
    __name__,
    description="Operations on tasks",
    url_prefix="/api"
)


def get_db():
    """Connect to the database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def row_to_dict(row):
    """Convert sqlite3.Row to dictionary with proper type conversion."""
    if row is None:
        return None
        
    result = {}
    for key in row.keys():
        # Handle special conversions based on key
        if key == 'status':
            result[key] = bool(row[key])
        else:
            result[key] = row[key]
    return result


@blp.route("/tasks")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        """Get all tasks."""
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'SELECT id, description, due_date, status, created_at FROM tasks ORDER BY created_at DESC'
            )
            rows = cursor.fetchall()
            
            # Convert each row to a dictionary
            result = []
            for row in rows:
                result.append(row_to_dict(row))
                
            # Return result directly as a list of dictionaries
            return result
            
        except Exception as e:
            current_app.logger.error(f"Error in GET /tasks: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=f"Database error: {str(e)}")

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        """Create a new task."""
        try:
            db = get_db()
            
            # Extract values from request
            description = task_data['description']
            due_date = task_data['due_date']
            status = 1 if task_data.get('status', False) else 0
            
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO tasks (description, due_date, status) VALUES (?, ?, ?)',
                (description, due_date, status)
            )
            task_id = cursor.lastrowid
            db.commit()
            
            # Fetch the new task
            cursor.execute(
                'SELECT id, description, due_date, status, created_at FROM tasks WHERE id = ?',
                (task_id,)
            )
            new_task = cursor.fetchone()
            
            # Convert to dict and return
            return row_to_dict(new_task)
            
        except Exception as e:
            db.rollback()
            current_app.logger.error(f"Error in POST /tasks: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=f"Database error: {str(e)}")


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        """Get a task by ID."""
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'SELECT id, description, due_date, status, created_at FROM tasks WHERE id = ?',
                (task_id,)
            )
            task = cursor.fetchone()
            
            if task is None:
                abort(404, message="Task not found")
                
            # Convert to dict and return
            return row_to_dict(task)
            
        except Exception as e:
            current_app.logger.error(f"Error in GET /tasks/{task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=f"Database error: {str(e)}")
    
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        """Update a task."""
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Check if task exists
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            if cursor.fetchone() is None:
                abort(404, message="Task not found")
            
            # Build update query
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
                params.append(1 if task_data['status'] else 0)
                
            if not update_fields:
                abort(400, message="No fields to update")
                
            # Execute update
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            params.append(task_id)
            cursor.execute(query, params)
            db.commit()
            
            # Fetch updated task
            cursor.execute(
                'SELECT id, description, due_date, status, created_at FROM tasks WHERE id = ?',
                (task_id,)
            )
            updated_task = cursor.fetchone()
            
            # Convert to dict and return
            return row_to_dict(updated_task)
            
        except Exception as e:
            db.rollback()
            current_app.logger.error(f"Error in PUT /tasks/{task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=f"Database error: {str(e)}")
    
    @blp.response(204)
    def delete(self, task_id):
        """Delete a task."""
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Check if task exists
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            if cursor.fetchone() is None:
                abort(404, message="Task not found")
                
            # Delete task
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            db.commit()
            return {}
            
        except Exception as e:
            db.rollback()
            current_app.logger.error(f"Error in DELETE /tasks/{task_id}: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            abort(500, message=f"Database error: {str(e)}")