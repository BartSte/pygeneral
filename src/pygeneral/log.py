"""Logging configuration with sane defaults."""

import logging
import os
from logging.handlers import RotatingFileHandler
from platform import platform

_FMT = "%(asctime)s - %(levelname)s - %(name)s@%(module)s.%(funcName)s:%(lineno)d - %(message)s"
_WIN_LOG_DIR = os.path.join(os.getenv("APPDATA", ""))
_UNIX_LOG_DIR = os.path.join(os.path.expanduser("~"), ".local", "share")


def setup(
    name: str | None = None,
    filename: str = "",
    fmt: str = _FMT,
    loglevel: int = logging.WARNING,
) -> logging.Logger:
    f"""Configure and return a logger with sensible defaults.

    Args:
        name: The logger name. Defaults to the module name when not provided.
        filename: Path to the log file. If empty, a default path is used which
        is:
            - On Windows: {_WIN_LOG_DIR}\\<name>.log
            - On Unix: {_UNIX_LOG_DIR}/<name>.log
        fmt: Log message format string. Default: {_FMT}.
        loglevel: Logging level to apply to the handlers and logger.
        propagate: Whether to propagate log messages to ancestor loggers.

    Returns:
        Configured logger with stream and optional file handlers.
    """
    filename = os.path.expandvars(os.path.expanduser(filename))
    filename = filename or _make_default_log_file(name or __name__)
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)

    handlers = _make_handlers(filename, loglevel, fmt)
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(loglevel)
    for handler in handlers:
        logger.addHandler(handler)

    logger.debug(
        f"Logger is setup with the following parameters: {name=}, {filename=}, "
        f"{fmt=}, {loglevel=}"
    )
    return logger


def _make_default_log_file(name: str) -> str:
    """Create a default log file path based on the OS."""
    if platform().startswith("Windows"):
        base_dir = os.path.join(os.getenv("APPDATA", ""))
    else:
        home = os.path.expanduser("~")
        base_dir = os.path.join(home, ".local", "share")
    return os.path.join(base_dir, f"{name}.log")


def _make_handlers(
    filename: str, loglevel: int, fmt: str
) -> list[logging.Handler]:
    """Create logging handlers for stream output and an optional rotating file.

    Args:
        filename: Path to the log file. If falsy, no file handler is created.
        loglevel: Logging level to apply to the handlers.
        fmt: Log message format string.

    Returns:
        list[logging.Handler]: Configured logging handlers.
    """
    formatter = logging.Formatter(fmt)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if filename:
        file_handler = RotatingFileHandler(
            filename,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
        )
        handlers.append(file_handler)

    for handler in handlers:
        handler.setLevel(loglevel)
        handler.setFormatter(formatter)

    return handlers
