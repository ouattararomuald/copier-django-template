[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
![Tests](https://github.com/ouattararomuald/copier-django-template/actions/workflows/tests.yml/badge.svg)

# Copier Django Template

A modern [Copier](https://github.com/copier-org/copier) template for scaffolding a Django project with best practices built-in.

## ✨ Features

### 🚀 Modern Django Stack
- **Django 4.2, 5.2, or 6.0** - Choose your preferred Django version
- **Django REST Framework** - Build powerful APIs with ease
- **JWT Authentication** - Secure token-based authentication via [djoser](https://djoser.readthedocs.io/)
- **Custom User Model** - Ready-to-extend user model included

### 🛠️ Developer Experience
- **[uv](https://github.com/astral-sh/uv)** - Lightning-fast Python package management
- **[ruff](https://github.com/astral-sh/ruff)** - Blazing-fast linting and formatting
- **[Task](https://taskfile.dev/)** - Simple task automation (no more long commands!)
- **[pytest](https://docs.pytest.org/)** - Modern testing with 100% starting coverage

### 🗄️ Database Options
- **PostgreSQL** (versions 16, 17, or 18) - Production-ready database
- **SQLite** - Zero-config option for quick prototyping

### 🐳 Docker Support
- **Docker Compose** - Pre-configured services for local development
- **PostgreSQL** - Containerized database
- **Redis** - Caching and session storage
- **[Mailpit](https://github.com/axllent/mailpit/)** - Email testing with web UI

### 🔧 Optional Enhancements
- **[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)** - Performance insights and debugging
- **[Django Extensions](https://django-extensions.readthedocs.io/)** - Enhanced management commands
- **[drf-spectacular](https://drf-spectacular.readthedocs.io/)** - Auto-generated OpenAPI/Swagger docs

### 🚦 CI/CD Ready
- **GitHub Actions** - Pre-configured workflows for:
  - Automated testing
  - Code linting and formatting checks
  - Migration checks
  - Security scanning with bandit

### 📦 Production Ready
- **Multiple Environments** - Separate settings for local, preprod, and production
- **Environment Variables** - Secure configuration management
- **Static Files** - Optimized with WhiteNoise
- **CORS Support** - Pre-configured for frontend integration
- **Security Best Practices** - Django security settings out of the box

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
# MacOS
brew install go-task

# Linux (using snap)
snap install task --classic

# Or using go
go install github.com/go-task/task/v3/cmd/task@latest

# Windows (using Chocolatey)
choco install go-task

# Or download binary from https://taskfile.dev/installation/
```

3. Generate your project

```bash
# Create in a new directory (my-project)
uvx copier copy https://github.com/ouattararomuald/copier-django-template my-project/ --trust

# Or create in current directory
mkdir my-project && cd my-project
uvx copier copy https://github.com/ouattararomuald/copier-django-template . --trust
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

## 📚 What You Get

After running the template, you'll have a fully functional Django project with:

```
my-project/
├── apps/                    # Your Django applications
│   ├── accounts/           # User authentication (JWT, registration, etc.)
│   ├── core/              # Shared utilities and base models
│   └── static/            # Static files
├── config/                 # Django configuration
│   ├── settings/          # Environment-specific settings
│   └── urls.py           # URL routing
├── compose/               # Docker Compose files
├── tests/                 # Shared test utilities
├── utils/                 # Pure python helpers
├── .github/workflows/     # CI/CD pipelines
├── manage.py             # Django management script
├── pyproject.toml        # Dependencies and tool configuration
├── Taskfile.yml          # Task automation
└── .env                  # Environment variables (created from .env.default)
```

## 🎯 Use Cases

This template is perfect for:

- 🌐 **REST APIs** - Build backend services for web and mobile apps
- 🔐 **Authentication Services** - JWT-based user management out of the box
- 🚀 **MVPs & Prototypes** - Get started quickly with best practices
- 🏢 **Enterprise Projects** - Multiple environments, CI/CD, security built-in

## 🤔 Why This Template?

- ✅ **Battle-tested** - Built on Django best practices
- ✅ **Modern tooling** - Uses the latest Python ecosystem tools
- ✅ **Comprehensive** - Everything you need, nothing you don't
- ✅ **Flexible** - Choose your Django version, database, and optional features
- ✅ **Well-tested** - Template itself has extensive test coverage
- ✅ **Maintained** - Regular updates for Django and dependency versions
- ✅ **Documented** - Clear README in generated projects


## 🔄 Keeping Your Project Updated

One of the best features of using Copier is the ability to update your project when the template improves:

```bash
# Update your project to the latest template version
uvx copier update

# Review changes and resolve any conflicts
# Copier will create .rej files for conflicts
```

This allows you to benefit from template improvements even after project creation!

## 🧪 Development and Customization

### Testing the Template

```bash
# Clone the repository
git clone https://github.com/ouattararomuald/copier-django-template.git
cd copier-django-template

# Install dependencies
uv sync

# Run template tests
uv run pytest

# Generate a test project
uv run copier copy . /tmp/my-test-project --trust --vcs-ref=HEAD
```

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) and [copier-python-template](https://github.com/gotofritz/copier-python-template)
- Built with [Copier](https://github.com/copier-org/copier)

## 📮 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/ouattararomuald/copier-django-template/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/ouattararomuald/copier-django-template/issues)
- 📖 **Documentation**: See generated project's README.md
- 🤝 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Happy coding! 🎉** If this template helps you, consider giving it a ⭐ on GitHub!
