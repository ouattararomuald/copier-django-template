# Contributing to Copier Django Template

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Enhancements

We welcome suggestions for new features or improvements! Please open an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create a new branch from `main`:
   ```bash
   git switch -c feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Run the template generation tests
   uv run pytest
   
   # Generate a test project and verify it works
   uv run copier copy . /tmp/test-project --trust --vcs-ref=HEAD
   cd /tmp/test-project
   uv sync
   uv run pytest
   ```

4. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Follow conventional commits format (optional but appreciated):
     - `feat:` for new features
     - `fix:` for bug fixes
     - `docs:` for documentation changes
     - `test:` for test changes
     - `refactor:` for code refactoring

5. **Push to your fork** and submit a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Describe your changes** in the PR description:
   - What changes were made and why
   - Any breaking changes
   - Related issues (use `Fixes #123` to auto-close issues)

## Development Setup

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ouattararomuald/copier-django-template.git
   cd copier-django-template
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run tests:
   ```bash
   uv run pytest
   ```

### Testing Your Changes

#### Test the Template Itself

```bash
# Run structure validation tests
uv run pytest tests/

# These tests verify that the template generates correctly
# for various configurations (Django versions, databases, etc.)
```

#### Test a Generated Project

```bash
# Generate a test project
uvx copier copy . /tmp/test-project --trust --vcs-ref=HEAD

# Navigate to the generated project
cd /tmp/test-project

# Install dependencies
uv sync

# Run the generated project's tests
uv run --env-file .env pytest

# Try running the server
uv run --env-file .env manage.py migrate
uv run --env-file .env manage.py runserver
```

## Template Structure

```
copier-django-template/
├── template/              # The actual template files
│   ├── apps/             # Django apps
│   ├── config/           # Django configuration
│   ├── *.jinja           # Jinja2 templates
│   └── ...
├── extensions/           # Copier extensions (context processors)
├── tests/               # Template generation tests
├── copier.yml          # Copier configuration
└── README.md           # Main documentation
```

### Key Files

- **`copier.yml`**: Defines template questions and configuration
- **`template/`**: Contains all files that will be copied to generated projects
- **`*.jinja` files**: Templates that are processed by Jinja2
- **`extensions/context.py`**: Custom Jinja2 extensions and context processors

## Guidelines

### Template Files

- Use `.jinja` extension for files that need template processing
- Use Jinja2 conditionals for optional features:
  ```jinja
  {% if use_django_toolbar %}
  # Django Debug Toolbar configuration
  {% endif %}
  ```

### Testing

- Add tests for new features in `tests/test_project_structure.py`
- Test multiple configurations (Django versions, databases, etc.)
- Ensure generated projects pass their own tests

### Documentation

- Update `README.md` for user-facing changes
- Update `template/README.md.jinja` if changes affect generated projects
- Add inline comments for complex template logic

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Keep functions small and focused
- Add docstrings for complex functions

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing! 🎉

