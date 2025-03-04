# claude_todo

A simple, elegant task management application built with Flask.

## Technical Stack

- **Backend Framework**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Version Control**: Git (GitHub repository)

## Database Design

The application uses a single SQLite database named `mytasks.db` with the following schema:

### Table: `tasks`

| Column       | Type    | Description                               |
|--------------|---------|-------------------------------------------|
| id           | INTEGER | Primary key, auto-increment               |
| description  | TEXT    | Text description of the task              |
| due_date     | DATE    | Due date for the task                     |
| status       | BOOLEAN | Task status (0 = not done, 1 = completed) |
| created_at   | DATETIME| When the task was created                 |

## Features

1. **Task Management**
   - Create new tasks with description and due date
   - Mark tasks as complete/incomplete
   - Delete tasks
   - View all tasks with pagination (10 tasks per page)

2. **User Interface**
   - Single page web application
   - Dark theme with a modern color palette
   - Completed tasks are displayed with strikethrough styling
   - Intuitive user interface with clear visual feedback
   - Pagination controls when task count exceeds 10

## Project Structure

```
claude_todo/
│
├── app.py                 # Main Flask application
├── schema.sql             # SQL schema for database initialization
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom CSS styling
│   └── js/
│       └── script.js      # Frontend JavaScript
│
├── templates/             # HTML templates
│   └── index.html         # Main application page
│
├── mytasks.db             # SQLite database
├── README.md              # Project documentation
├── howtouse.txt           # User guide
└── requirements.txt       # Python dependencies
```

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/claude_todo.git
   cd claude_todo
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   flask init-db
   ```

4. Run the application:
   ```
   flask run
   ```

5. Access the application at http://127.0.0.1:5000

## Development Guidelines

### UI Design

- Use a dark theme with the following color palette:
  - Background: #1e1e2e
  - Text: #cdd6f4
  - Accent: #89b4fa
  - Success: #a6e3a1
  - Warning: #f9e2af
  - Error: #f38ba8

- Task status should be visually distinct:
  - Completed tasks: Strikethrough text, dimmed appearance
  - Upcoming tasks: Regular text
  - Overdue tasks: Highlighted with warning color

### Functionality Requirements

- Maximum of 10 tasks displayed per page
- Pagination controls should appear when there are more than 10 tasks
- Task sorting by due date (ascending by default)
- Ability to filter tasks by status (all, complete, incomplete)
- Simple, intuitive controls for task management

### Version Control

- Commit messages should be clear and descriptive
- Follow the conventional commits format: `type(scope): message`
- Branch strategy: main for stable releases, develop for ongoing development

## User Documentation

Upon completion of the project, a user guide (howtouse.txt) should be generated that explains:

- How to add tasks
- How to mark tasks as complete/incomplete
- How to delete tasks
- How to navigate between pages
- Any additional features implemented
