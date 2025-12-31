import os
import subprocess
import sys
from pathlib import Path
from typing import Union, Any

import pytest
from copier import run_copy

from tests.types import File

PY312 = sys.version_info[:2] == (3, 12)
PY313 = sys.version_info[:2] == (3, 13)


def generate_project(root_path: str, dest: Path, data: dict[str, Any]) -> None:
    """Helper to run copier with sanitized environment."""
    run_copy(
        src_path=root_path,
        dst_path=dest,
        data=data,
        vcs_ref="HEAD",
        skip_tasks=False,
        unsafe=True,
    )


def assert_project_structure(base: Path, spec: dict[str, Union[File, dict]]):
    """
    Validates the project structure using flat paths.
    """
    for path_str, expectation in spec.items():
        p = base / path_str

        assert p.exists(), f"Path missing: {path_str}"

        if isinstance(expectation, File):
            assert p.is_file(), f"Expected file, found directory: {path_str}"

            if expectation.is_binary:
                if expectation.must_have_content:
                    assert p.stat().st_size > 0, f"Binary file {path_str} is empty"
                continue

            content = p.read_text(encoding="utf-8")
            if expectation.must_have_content:
                assert content.strip() != "", f"File is empty: {path_str}"

            if expectation.contains:
                for snippet in expectation.contains:
                    assert snippet in content, (
                        f"Snippet '{snippet}' not found in {path_str}"
                    )

        elif isinstance(expectation, dict):
            assert p.is_dir(), f"Expected directory: {path_str}"


@pytest.mark.parametrize(
    "database_engine,postgres_version,django_version,add_optional_dependencies",
    [
        pytest.param(
            "postgres",
            17,
            "4.2",
            True,
            marks=pytest.mark.skipif(
                not PY312,
                reason="Django 4.2 scenario is only supported on Python 3.12 in this test matrix",
            ),
        ),
        pytest.param(
            "postgres",
            17,
            "5.2",
            True,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 5.2 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
        pytest.param(
            "postgres",
            17,
            "6.0",
            True,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 6.0 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
        pytest.param(
            "postgres",
            17,
            "6.0",
            False,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 6.0 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),

        pytest.param(
            "sqlite",
            17,
            "4.2",
            True,
            marks=pytest.mark.skipif(
                not PY312,
                reason="Django 4.2 scenario is only supported on Python 3.12 in this test matrix",
            ),
        ),
        pytest.param(
            "sqlite",
            17,
            "5.2",
            True,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 5.2 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
        pytest.param(
            "sqlite",
            17,
            "6.0",
            True,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 6.0 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
        pytest.param(
            "sqlite",
            17,
            "6.0",
            False,
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 6.0 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
    ],
)
def test_defaults(
    root_path: str,
    tmp_path: Path,
    answers: dict[str, Any],
    database_engine: str,
    postgres_version: int,
    django_version: str,
    add_optional_dependencies: bool,
) -> None:
    # Set up answers
    answers.update(
        {
            "django_version": django_version,
            "database_engine": database_engine,
            "use_django_toolbar": add_optional_dependencies,
            "use_django_extensions": add_optional_dependencies,
            "use_drf_spectacular": add_optional_dependencies,
            "python_version": "3.12" if django_version == "4.2" else "3.13",
        }
    )

    if database_engine == "postgres":
        answers["postgres_version"] = postgres_version

    destination_path = tmp_path / "generated_project"
    generate_project(root_path, destination_path, answers)

    project_name = answers["project_name"]
    project_description = answers["project_description"]
    project_version = answers["project_version"]

    db_engine_str = "postgresql" if database_engine == "postgres" else "sqlite3"

    expected_base_settings = [
        f'"ENGINE": "django.db.backends.{db_engine_str}"',
        "corsheaders",
        "rest_framework",
        "apps.core",
        "apps.accounts",
        "corsheaders",
        "rest_framework",
        "rest_framework_simplejwt",
        "rest_framework_simplejwt.token_blacklist",
        "rest_framework.authtoken",
        "djoser",
        "whitenoise",
        "apps.core",
        "apps.accounts",
        '"ACCESS_TOKEN_LIFETIME": timedelta(minutes=15)',
        '"REFRESH_TOKEN_LIFETIME": timedelta(days=7)',
        '"ROTATE_REFRESH_TOKENS": True',
        '"BLACKLIST_AFTER_ROTATION": True',
        '"SEND_ACTIVATION_EMAIL": True',
        '"SEND_CONFIRMATION_EMAIL": True',
        '"HIDE_USERS": True',
    ]

    py_project_deps = [f"django~={django_version}"]
    if database_engine == "postgres":
        py_project_deps.append("psycopg[binary]")

    if add_optional_dependencies:
        py_project_deps.append("django-debug-toolbar")
        py_project_deps.append("django-extensions")
        py_project_deps.append("drf-spectacular")

    expected_docker_compose_content = [
        "redis:",
        "mailpit:",
    ]

    expected_preprod_settings = ["DEBUG = True"]

    if add_optional_dependencies:
        debug_toolbar_settings = [
            "debug_toolbar",
            "debug_toolbar.middleware.DebugToolbarMiddleware",
            'INTERNAL_IPS = ["127.0.0.1"]',
        ]
        django_extensions_settings = ["django_extensions"]
        drf_spectacular_settings = [
            "drf_spectacular",
            "REST_FRAMEWORK = {",
            "**REST_FRAMEWORK",
            '"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"',
            "SPECTACULAR_SETTINGS = {",
            f'"TITLE": "{project_name} API"',
            f'"DESCRIPTION": "{project_description}"',
            f'"VERSION": "{project_version}"',
        ]

        expected_preprod_settings.extend(debug_toolbar_settings)
        expected_preprod_settings.extend(django_extensions_settings)
        expected_preprod_settings.extend(drf_spectacular_settings)

    project_spec = {
        # .github
        ".github/workflows/linter.yml": File(),
        ".github/workflows/migrations-check.yml": File(),
        ".github/workflows/tests.yml": File(),
        # apps
        "apps/accounts/migrations/0001_initial.py": File(),
        "apps/accounts/migrations/__init__.py": File(must_have_content=False),
        "apps/accounts/models/__init__.py": File(must_have_content=False),
        "apps/accounts/models/user.py": File(),
        "apps/accounts/tests/__init__.py": File(must_have_content=False),
        "apps/accounts/tests/test_jwt_endpoints.py": File(),
        "apps/accounts/tests/test_user_detail.py": File(),
        "apps/accounts/tests/test_user_list.py": File(),
        "apps/accounts/tests/test_user_me.py": File(),
        "apps/accounts/tests/test_user_password.py": File(),
        "apps/accounts/tests/test_user_username.py": File(),
        "apps/accounts/__init__.py": File(must_have_content=False),
        "apps/accounts/admin.py": File(),
        "apps/accounts/apps.py": File(),
        "apps/accounts/views.py": File(),
        "apps/core/__init__.py": File(must_have_content=False),
        "apps/core/apps.py": File(),
        "apps/core/fields.py": File(),
        "apps/static/image/favicons/favicon.ico": File(is_binary=True),
        "apps/__init__.py": File(must_have_content=False),
        # compose
        "compose/local/docker-compose.yml": File(
            contains=expected_docker_compose_content
        ),
        # config
        "config/settings/base.py": File(contains=expected_base_settings),
        "config/settings/local.py": File(contains=expected_preprod_settings),
        "config/settings/preprod.py": File(contains=expected_preprod_settings),
        "config/settings/production.py": File(contains=["DEBUG = False"]),
        "config/settings/test.py": File(),
        "config/tests/__init__.py": File(must_have_content=False),
        "config/tests/test_logging.py": File(),
        "config/__init__.py": File(must_have_content=False),
        "config/asgi.py": File(),
        "config/logging.py": File(),
        "config/urls.py": File(),
        "config/wsgi.py": File(),
        # taskfiles
        "taskfiles/Check.yml": File(),
        "taskfiles/Django.yml": File(),
        "taskfiles/Docker.yml": File(),
        "taskfiles/Lint.yml": File(),
        "taskfiles/Test.yml": File(),
        # tests
        "tests/assertions/__init__.py": File(must_have_content=False),
        "tests/assertions/email_assertions.py": File(),
        "tests/fixtures/__init__.py": File(must_have_content=False),
        "tests/fixtures/user.py": File(),
        "tests/__init__.py": File(must_have_content=False),
        "tests/common.py": File(),
        # utils
        "utils/__init__.py": File(must_have_content=False),
        "utils/README.md": File(),
        # other files
        ".env.default": File(),
        ".gitignore": File(),
        "conftest.py": File(),
        "manage.py": File(),
        "pyproject.toml": File(contains=py_project_deps),
        "README.md": File(),
        "Taskfile.yml": File(),
    }

    assert_project_structure(destination_path, project_spec)


@pytest.mark.parametrize(
    "database_engine,django_version,python_version",
    [
        pytest.param(
            "postgres",
            "4.2",
            "3.12",
            marks=pytest.mark.skipif(
                not PY312,
                reason="Django 4.2 scenario is only supported on Python 3.12 in this test matrix",
            ),
        ),

        pytest.param(
            "postgres",
            "5.2",
            "3.13",
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 5.2 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
        pytest.param(
            "postgres",
            "6.0",
            "3.13",
            marks=pytest.mark.skipif(
                not PY313,
                reason="Django 6.0 scenario is only supported on Python 3.13 in this test matrix",
            ),
        ),
    ],
)
def test_generated_project_tests_execution(
    root_path: str,
    tmp_path: Path,
    answers: dict[str, Any],
    database_engine: str,
    django_version: str,
    python_version: str,
) -> None:
    answers.update(
        {
            "django_version": django_version,
            "database_engine": database_engine,
            "python_version": python_version,
            "project_name": "postgres",
            "use_django_toolbar": True,
            "use_django_extensions": True,
            "use_drf_spectacular": True,
        }
    )

    if database_engine == "postgres":
        answers["postgres_version"] = 17

    destination_path = tmp_path / "generated_project"
    generate_project(root_path, destination_path, answers)

    run_generated_project_tests(destination_path)


def run_command(cwd: Path | str | bytes, args: list[str], error_msg: str) -> None:
    """Executes a shell command and fails the test if it returns a non-zero exit code.

    Args:
        cwd: The working directory where the command should be executed.
        args: A list of command-line arguments (e.g., ["uv", "run", "pytest"]).
        error_msg: A descriptive message to display if the command fails.

    Raises:
        pytest.fail.Exception: If the process returns a non-zero exit code,
            providing the exit code, STDOUT, and STDERR in the failure message.
    """
    result = subprocess.run(
        args=args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        pytest.fail(
            f"{error_msg} with return code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )


def run_generated_project_tests(project_path: Path):
    """Runs pytest inside the generated project."""
    run_command(
        cwd=project_path,
        args=["task", "test:coverage", "--", "--cov-fail-under=100"],
        error_msg="Tests in generated project failed",
    )

    run_command(
        cwd=project_path,
        args=["task", "lint"],
        error_msg="Quality checks in generated project failed",
    )

    if bool(os.environ.get("CI", "false") == "true"):
        run_command(
            cwd=project_path,
            args=["task", "checks:migrations:check"],
            error_msg="Django migrations check in generated project failed",
        )
