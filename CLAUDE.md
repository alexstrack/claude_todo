# Claude Helper Reference

## Commands
- **Setup**: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- **Run**: `flask run`
- **Initialize DB**: `flask init-db`
- **Test**: `pytest` (add specific test with `pytest tests/test_file.py::test_function`)
- **Lint**: `flake8 --max-line-length=100`
- **Type Check**: `mypy --ignore-missing-imports .`

## Code Style
- **Python**: Follow PEP 8 standards. Maximum line length 100.
- **Imports**: Group standard library, third-party, and local imports with a blank line between groups.
- **Formatting**: Use 4 spaces for indentation. Use trailing commas in multi-line structures.
- **Naming**: snake_case for variables/functions, CamelCase for classes, UPPER_CASE for constants.
- **Error Handling**: Use try/except blocks with specific exceptions. Log errors appropriately.
- **Comments**: Docstrings for all functions/classes. Comments for complex logic only.
- **Git**: Use conventional commits format: `type(scope): message`

## UI Theme
- Dark theme with colors: Background #1e1e2e, Text #cdd6f4, Accent #89b4fa
- Success #a6e3a1, Warning #f9e2af, Error #f38ba8