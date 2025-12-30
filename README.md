[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
![Tests](https://github.com/ouattararomuald/copier-django-template/actions/workflows/tests.yml/badge.svg)

# Cookiecutter Django DRF

A modern [Copier](https://github.com/copier-org/copier) template for scaffolding a Django project with best practices built-in.

## Features

- Modern python packaging using [uv](https://github.com/astral-sh/uv)
- Code formatting and linting with [ruff](https://github.com/astral-sh/ruff)
- Streamlined task execution with [Task](https://taskfile.dev/)
- Customizable Django version 4.2 or above
- Customizable python version
- Customizable PostgreSQL version
- Renders Django projects with 100% starting test coverage
- Optimized development and production settings
- Registration via [djoser](https://djoser.readthedocs.io/en/latest/)
- Comes with a custom user model ready to go
- Docker support using [docker-compose](https://github.com/docker/compose) for development 
- Run with [pytest](https://docs.pytest.org/en/stable/)
- Continuous integration with [GitHub Actions](https://docs.github.com/en/actions)
- Integration with [Mailpit](https://github.com/axllent/mailpit/) for local email testing

## Quick Start

### Creating a new django project

1. Install UV

```bash
# MacOS or Linux
curl -LsSf https://astral.sh/uv/install.sh | less

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

2. Install Taskfile (Optional but recommended)

```bash

```

3. Generate your project

```bash
# Create in a new directory (my-project)
uvx copier copy https://github.com/ouattararomuald/copier-django-template my-project/ --trust

# Or create in current directory
mkdir my-project && cd my-project
uvx copier copy https://github.com/gotofritz/copier-python-template . --trust
```

> Note: The `--trust` flag is required as the template executes setup scripts.

4. **Configure your project** by answering the interactive prompts.
5. Initialize git and create a remote repository

```bash
cd my-project
git init

# Using GitHub CLI (recommended)
gh repo create my-org/my-project --private --source=. --push

# Or follow GitHub's instructions to push an existing repository
```

6. Set up dependencies

```bash
uv sync
git add uv.lock && git commit -m "feat: add dependency lock file"
```

### Updating your project

Keep your project aligned with the latest template improvements:

```bash
uvx copier update
```

If conflicts arise, resolve them by inspecting the generated `.rej` files.

## Development and Customization

To test modifications to this template:

```bash
uv run copier copy ./copier-django-drf-template --trust --vcs-ref=HEAD my-test-project
```
