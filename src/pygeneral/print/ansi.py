import sys
from typing import TextIO

CLEAR_LINE = "\033[K"
HIDE_CURSOR = "\033[?25l"
MOVE_UP = "\033[F"
SHOW_CURSOR = "\033[?25h"


def _print(
    message: str,
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Wrapper for the print function with convenient defaults.

    Args:
        message (str): The message to print.
        end (str, optional): The string to print at the end. Defaults to "".
        file (file, optional): The file to print to. Defaults to sys.stderr.
        flush (bool, optional): Whether to flush the output. Defaults to True.
        kwargs: Additional keyword arguments to pass to the print function.
    """
    print(message, end=end, file=file, flush=flush, **kwargs)


def hide_cursor(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Hide the cursor."""
    _print(HIDE_CURSOR, end=end, file=file, flush=flush, **kwargs)


def move_up(
    count: int = 1,
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Move the cursor up."""
    _print(MOVE_UP * count, end=end, file=file, flush=flush, **kwargs)


def show_cursor(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Show the cursor."""
    _print(SHOW_CURSOR, end=end, file=file, flush=flush, **kwargs)


def clear_line(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Clear the current line."""
    _print(CLEAR_LINE, end=end, file=file, flush=flush, **kwargs)
