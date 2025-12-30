import os
import subprocess
from pathlib import Path
from typing import Union, Any

import pytest
from copier import run_copy

from tests.types import File


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
                    assert snippet in content, f"Snippet '{snippet}' not found in {path_str}"

        elif isinstance(expectation, dict):
            assert p.is_dir(), f"Expected directory: {path_str}"

@pytest.mark.parametrize(
    "database_engine,postgres_version,django_version,add_optional_dependencies",
    [
        ("postgres", 16, "4.2", True), ("postgres", 17, "4.2", True), ("postgres", 18, "4.2", True),
        ("postgres", 16, "5.2", True), ("postgres", 17, "5.2", True), ("postgres", 18, "5.2", True),
        ("postgres", 16, "6.0", True), ("postgres", 17, "6.0", True), ("postgres", 18, "6.0", True),
        ("postgres", 16, "6.0", False), ("postgres", 17, "6.0", False), ("postgres", 18, "6.0", False),

        ("sqlite", 16, "4.2", True), ("sqlite", 17, "4.2", True), ("sqlite", 18, "4.2", True),
        ("sqlite", 16, "5.2", True), ("sqlite", 17, "5.2", True), ("sqlite", 18, "5.2", True),
        ("sqlite", 16, "6.0", True), ("sqlite", 17, "6.0", True), ("sqlite", 18, "6.0", True),
        ("sqlite", 16, "6.0", False), ("sqlite", 17, "6.0", False), ("sqlite", 18, "6.0", False),
    ]
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
    if database_engine == "postgres":
        answers["postgres_version"] = postgres_version
    answers["django_version"] = django_version
    answers["database_engine"] = database_engine
    answers["use_django_toolbar"] = add_optional_dependencies
    answers["use_django_extensions"] = add_optional_dependencies
    answers["use_drf_spectacular"] = add_optional_dependencies
    project_name = answers["project_name"]
    project_description = answers["project_description"]
    project_version = answers["project_version"]

    # Ensure python_version is compatible with Django version for the prompt
    if django_version == "4.2":
        answers["python_version"] = "3.12"
    else:
        answers["python_version"] = "3.13"

    destination_path = tmp_path / "generated_project"
    run_copy(
        src_path=root_path,
        dst_path=destination_path,
        data=answers,
        vcs_ref="HEAD",
        skip_tasks=False,
        unsafe=True,
    )

    if database_engine == "postgres":
        expected_database = (
            '"ENGINE": "django.db.backends.postgresql"'
        )
        docker_expected_postgres = f"{postgres_version}-alpine"
    else:
        expected_database = (
            '"ENGINE": "django.db.backends.sqlite3"'
        )
        docker_expected_postgres = None

    expected_base_settings_content = [
        expected_database,
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

    docker_compose_expected_content = [
        "redis:",
        "mailpit:",
    ]
    if docker_expected_postgres:
        docker_compose_expected_content.append(docker_expected_postgres)

    py_project_expected_dependencies = [
        f"django~={django_version}",
    ]

    if database_engine == "postgres":
        py_project_expected_dependencies.append("psycopg[binary]")

    if add_optional_dependencies:
        py_project_expected_dependencies.append("django-debug-toolbar")
        py_project_expected_dependencies.append("django-extensions")
        py_project_expected_dependencies.append("drf-spectacular")

    expected_preprod_settings_content = ["DEBUG = True"]

    if add_optional_dependencies:
        expected_preprod_settings_content.extend([
            "debug_toolbar",
            "debug_toolbar.middleware.DebugToolbarMiddleware",
            'INTERNAL_IPS = ["127.0.0.1"]',
        ])
        expected_preprod_settings_content.extend(["django_extensions"])
        expected_preprod_settings_content.extend([
            "drf_spectacular",
            "REST_FRAMEWORK = {",
            "**REST_FRAMEWORK",
            '"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"',
            "SPECTACULAR_SETTINGS = {",
            f'"TITLE": "{project_name} API"',
            f'"DESCRIPTION": "{project_description}"',
            f'"VERSION": "{project_version}"',
        ])

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
        "compose/local/docker-compose.yml": File(contains=docker_compose_expected_content),
        # config
        "config/settings/base.py": File(contains=[*expected_base_settings_content]),
        "config/settings/local.py": File(contains=[*expected_preprod_settings_content]),
        "config/settings/preprod.py": File(contains=[*expected_preprod_settings_content]),
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
        "pyproject.toml": File(contains=py_project_expected_dependencies),
        "Taskfile.yml": File(),
    }

    assert_project_structure(destination_path, project_spec)


@pytest.mark.parametrize(
    "database_engine,postgres_version,django_version,python_version",
    [
        ("postgres", 17, "5.2", "3.13"), ("postgres", 18, "6.0", "3.13"),
    ]
)
def test_generated_project_tests_execution(
    root_path: str,
    tmp_path: Path,
    answers: dict[str, Any],
    database_engine: str,
    postgres_version: int,
    django_version: str,
    python_version: str,
) -> None:
    if database_engine == "postgres":
        answers["postgres_version"] = postgres_version
    answers["django_version"] = django_version
    answers["database_engine"] = database_engine
    answers["python_version"] = python_version
    answers["use_django_toolbar"] = True
    answers["use_django_extensions"] = True
    answers["use_drf_spectacular"] = True
    answers["project_name"] = "postgres"

    destination_path = tmp_path / "generated_project"
    run_copy(
        src_path=root_path,
        dst_path=destination_path,
        data=answers,
        vcs_ref="HEAD",
        skip_tasks=False,
        unsafe=True,
    )

    run_generated_project_tests(destination_path)


def run_generated_project_tests(project_path: Path):
    """Runs pytest inside the generated project."""
    test_env = os.environ.copy()
    test_env["DJANGO_SETTINGS_MODULE"] = "config.settings.test"

    result = subprocess.run(
        ["cp", ".env.default", ".env"],
        cwd=project_path,
        capture_output=True,
        text=True,
        env=test_env,
    )

    if result.returncode != 0:
        pytest.fail(
            f"Copy of .env.default in generated project failed with return code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    result = subprocess.run(
        ["task", "test:coverage", "--", "--cov-fail-under=100"],
        cwd=project_path,
        capture_output=True,
        text=True,
        env=test_env,
    )

    if result.returncode != 0:
        pytest.fail(
            f"Tests in generated project failed with return code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    result = subprocess.run(
        ["task", "lint"],
        cwd=project_path,
        capture_output=True,
        text=True,
        env=test_env,
    )

    if result.returncode != 0:
        pytest.fail(
            f"Quality checks in generated project failed with return code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    if bool(os.environ.get("CI", "false") == "true"):
        result = subprocess.run(
            ["task", "checks:migrations:check"],
            cwd=project_path,
            capture_output=True,
            text=True,
            env=test_env,
        )

        if result.returncode != 0:
            pytest.fail(
                f"Django migrations check in generated project failed with return code {result.returncode}.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )
