# Cookiecutter Django DRF

A modern Django REST Framework starter template for building production-ready APIs with authentication, documentation, 
and best practices built-in.

## Features

- For Django 5 or above
- Works with python 3.13
- Renders Django projects with 100% starting test coverage
- Optimized development and production settings
- Registration via [djoser](https://djoser.readthedocs.io/en/latest/)
- Comes with a custom user model ready to go
- Docker support using [docker-compose](https://github.com/docker/compose) for development 
- Run with pytest
- Customizable PostgreSQL version
- [Taskfile](https://taskfile.dev/) integration
- Integration with [Mailpit](https://github.com/axllent/mailpit/) for local email testing

## Optional Integration

_These features can be enabled during initial project setup._

- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
- [django-extensions](https://django-extensions.readthedocs.io/en/latest/#getting-started)
- [drf_spectacular](https://drf-spectacular.readthedocs.io/en/latest/)

## Constraints

- The template relies only on actively maintained third-party libraries.

## Usage

Assume you want to bootstrap a Django project named `twitterclone`. Instead of running `django-admin startproject` 
and then manually adding the same metadata and configuration you inevitably forget until it hurts, you can generate 
a complete baseline in one pass with [Cookiecutter](https://github.com/cookiecutter/cookiecutter).

### 1) Install Cookiecutter:

`uv tool install "cookiecutter>=1.7.0"`

### 2) Generate a project from this template:

`uvx cookiecutter https://github.com/ouattararomuald/cookiecutter-django-drf`

Cookiecutter will ask you a series of questions (project name, configuration choices, etc.). Once you answer them, 
it will scaffold a ready-to-run Django project in a new folder.

> Note: If the generated files contain placeholders such as 'Romuald OUATTARA', replace them with your own details.

### 3) Inspect the generated project

`cd twitterclone/`

Review the generated structure and read the project’s README carefully.

### 4) Initialize Git and push to a remote

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin git@github.com:<username>/twitterclone.git
git push -u origin main
```
