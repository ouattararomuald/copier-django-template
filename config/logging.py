"""A module for logging utilities."""

import logging
import os

import structlog


def _get_exception_formatter() -> structlog.typing.ExceptionRenderer:
    """Return an exception formatter for structlog based on available libraries."""
    try:
        # Try to use rich for even better tracebacks
        from rich.traceback import install

        install(show_locals=True)
        exception_formatter = structlog.dev.rich_traceback
    except ImportError:
        # Fallback to structlog's built-in formatter
        exception_formatter = structlog.dev.plain_traceback

    return exception_formatter


def _get_renderer(debug: bool = False) -> structlog.typing.Processor:
    """Return a renderer for structlog."""
    log_format = os.getenv("LOG_FORMAT", "json" if not debug else "console")

    if log_format == "console":
        exception_formatter = _get_exception_formatter()

        renderer = structlog.dev.ConsoleRenderer(
            columns=[
                structlog.dev.Column(
                    "timestamp",
                    structlog.dev.KeyValueColumnFormatter(
                        key_style=None,
                        value_style=structlog.dev.YELLOW,
                        reset_style=structlog.dev.RESET_ALL,
                        value_repr=str,
                    ),
                ),
                structlog.dev.Column(
                    "level",
                    structlog.dev.KeyValueColumnFormatter(
                        key_style=None,
                        prefix="[",
                        postfix="]",
                        value_style=structlog.dev.GREEN,
                        reset_style=structlog.dev.RESET_ALL,
                        value_repr=str,
                    ),
                ),
                structlog.dev.Column(
                    "logger",
                    structlog.dev.KeyValueColumnFormatter(
                        key_style=None,
                        prefix="[",
                        postfix="]",
                        value_style=structlog.dev.BLUE,
                        reset_style=structlog.dev.RESET_ALL,
                        value_repr=str,
                    ),
                ),
                structlog.dev.Column(
                    "event",
                    structlog.dev.KeyValueColumnFormatter(
                        key_style=None,
                        value_style=structlog.dev.BRIGHT,
                        reset_style=structlog.dev.RESET_ALL,
                        value_repr=str,
                    ),
                ),
                # Everything else
                structlog.dev.Column(
                    "",
                    structlog.dev.KeyValueColumnFormatter(
                        key_style=structlog.dev.CYAN,
                        value_style=structlog.dev.GREEN,
                        reset_style=structlog.dev.RESET_ALL,
                        value_repr=repr,
                    ),
                ),
            ],
            sort_keys=False,
            exception_formatter=exception_formatter,
        )
    else:
        renderer = structlog.processors.JSONRenderer()

    return renderer


def configure_logging(debug: bool = False):
    """Configure structlog for the application."""
    if structlog.is_configured():
        return

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    renderer = _get_renderer(debug=debug)

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    log_level_name = os.environ.get("LOG_LEVEL", "DEBUG" if debug else "INFO")
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)


def get_logger(name: str | None = None):
    """
    Get a structlog logger instance.

    Args:
        name: Logger name, typically __name__

    Returns:
        Configured structlog logger

    Example:
        >>> from apps.common.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("user_created", user_id=123)
    """
    return structlog.get_logger(name)
