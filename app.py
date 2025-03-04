import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, jsonify, abort
from flask.cli import with_appcontext
import click


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'mytasks.db'),
)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


def get_db():
    """Connect to the database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database."""
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# Set up CLI commands
init_app(app)


@app.route('/')
def index():
    """Display the main page with all tasks."""
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Get total number of tasks for pagination
    total_tasks = db.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    total_pages = (total_tasks + per_page - 1) // per_page
    
    # Get tasks for current page
    tasks = db.execute(
        'SELECT id, description, due_date, status, created_at FROM tasks '
        'ORDER BY due_date ASC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    
    return render_template('index.html', 
                           tasks=tasks, 
                           page=page, 
                           total_pages=total_pages)


@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    description = request.form['description']
    due_date = request.form['due_date']
    
    if not description or not due_date:
        return jsonify({'error': 'Description and due date are required'}), 400
    
    db = get_db()
    db.execute(
        'INSERT INTO tasks (description, due_date) VALUES (?, ?)',
        (description, due_date)
    )
    db.commit()
    
    return redirect(url_for('index'))


@app.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """Toggle the status of a task."""
    db = get_db()
    
    # Get current status
    task = db.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        abort(404)
    
    # Toggle status
    new_status = 0 if task['status'] else 1
    
    db.execute(
        'UPDATE tasks SET status = ? WHERE id = ?',
        (new_status, task_id)
    )
    db.commit()
    
    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    
    return redirect(url_for('index'))


@app.template_filter('format_date')
def format_date(date_str):
    """Format a date string for display."""
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date_obj = date_str
    return date_obj.strftime('%b %d, %Y')


@app.template_filter('is_overdue')
def is_overdue(date_str, status):
    """Check if a task is overdue."""
    if status:  # Completed tasks can't be overdue
        return False
        
    if isinstance(date_str, str):
        due_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        due_date = date_str
        
    today = datetime.now().date()
    return due_date < today


if __name__ == '__main__':
    app.run(debug=True)