import sys
from typing import TextIO

CLEAR_LINE = "\033[K"
HIDE_CURSOR = "\033[?25l"
MOVE_UP = "\033[F"
SHOW_CURSOR = "\033[?25h"


def hide_cursor(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Hide the cursor.

    Args:
        end (str, optional): The string to print after the ANSI escape code.
        Defaults to "".
        file (TextIO, optional): The file to print to. Defaults to sys.stderr.
        flush (bool, optional): Whether to flush the file after printing.
        Defaults to True.
        **kwargs: Additional keyword arguments to pass to the print function.
    """
    print(HIDE_CURSOR, end=end, file=file, flush=flush, **kwargs)


def move_up(
    count: int = 1,
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Move the cursor up by `count` lines.

    Args:
        count (int, optional): The number of lines to move up. Defaults to 1.
        end (str, optional): The string to print after the ANSI escape code.
        Defaults to "".
        file (TextIO, optional): The file to print to. Defaults to sys.stderr.
        flush (bool, optional): Whether to flush the file after printing.
        Defaults to True.
        **kwargs: Additional keyword arguments to pass to the print function.
    """
    print(MOVE_UP * count, end=end, file=file, flush=flush, **kwargs)


def show_cursor(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Show the cursor.

    Args:
        end (str, optional): The string to print after the ANSI escape code.
        Defaults to "".
        file (TextIO, optional): The file to print to. Defaults to sys.stderr.
        flush (bool, optional): Whether to flush the file after printing.
        Defaults to True.
        **kwargs: Additional keyword arguments to pass to the print function.
    """
    print(SHOW_CURSOR, end=end, file=file, flush=flush, **kwargs)


def clear_line(
    end: str = "",
    file: TextIO = sys.stderr,
    flush: bool = True,
    **kwargs: str | None,
):
    """Clear the current line.

    Args:
        end (str, optional): The string to print after the ANSI escape code.
        Defaults to "".
        file (TextIO, optional): The file to print to. Defaults to sys.stderr.
        flush (bool, optional): Whether to flush the file after printing.
        Defaults to True.
        **kwargs: Additional keyword arguments to pass to the print function.
    """
    print(CLEAR_LINE, end=end, file=file, flush=flush, **kwargs)
