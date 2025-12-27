import json
import logging
from unittest.mock import MagicMock, patch

import pytest
import structlog

import apps.common.logging as logmod


@pytest.fixture(autouse=True)
def reset_logging():
    """Keep tests isolated by resetting logging and structlog."""
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(logging.NOTSET)
    structlog.reset_defaults()
    yield
    structlog.reset_defaults()


@pytest.mark.parametrize(
    "env_format, debug, expected_type",
    [
        (None, False, structlog.processors.JSONRenderer),
        (None, True, structlog.dev.ConsoleRenderer),
        ("console", False, structlog.dev.ConsoleRenderer),
        ("json", True, structlog.processors.JSONRenderer),
    ],
)
def test_get_renderer(monkeypatch, env_format, debug, expected_type):
    if env_format:
        monkeypatch.setenv("LOG_FORMAT", env_format)
    else:
        monkeypatch.delenv("LOG_FORMAT", raising=False)

    assert isinstance(logmod._get_renderer(debug=debug), expected_type)


def test_exception_formatter_falls_back_without_rich():
    with patch.dict("sys.modules", {"rich.traceback": None}):
        assert logmod._get_exception_formatter() is structlog.dev.plain_traceback


def test_exception_formatter_uses_rich_when_available(monkeypatch):
    mock_install = MagicMock()
    mock_rich_traceback = MagicMock()

    with patch.dict("sys.modules", {"rich.traceback": MagicMock(install=mock_install)}):
        monkeypatch.setattr(structlog.dev, "rich_traceback", mock_rich_traceback)
        assert logmod._get_exception_formatter() is mock_rich_traceback
        mock_install.assert_called_once_with(show_locals=True)


def test_configure_structlog_output(monkeypatch, capsys):
    monkeypatch.setenv("LOG_FORMAT", "json")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    logmod.configure_structlog(debug=False)
    logger = logmod.get_logger("test")

    logger.info("hello", foo="bar")
    logger.debug("should_not_show")

    out = capsys.readouterr().err.strip().splitlines()
    assert len(out) == 1
    payload = json.loads(out[0])
    assert payload["event"] == "hello"
    assert payload["foo"] == "bar"
