import re
from typing import Callable


def lensort(lines: str, regex: str) -> str:
    r"""
    Sort the lines based on the number of characters before the regular
    expression match is found. The lines with the least number of characters
    before the regular expression match are moved to the top, and the lines
    with the most number of characters before the regular expression match are
    moved to the bottom. Lines with no match are moved to the top.

    The lines are first sorted based on the total number of characters. This
    ensures that lines with the same number of characters are sorted based on
    their total length.

    Args:
    ----
        lines: lines of text separated by a newline.
        regex: the regular expression

    Returns:
    -------
        sorted variable definitions separated by a newline.

    """
    len_to_match: Callable[[str], int] = _make_len_to_match(regex)

    as_list = lines.splitlines()
    as_list.sort(key=len)
    as_list.sort(key=len_to_match)
    return "\n".join(as_list)


def _make_len_to_match(regex: str) -> Callable[[str], int]:
    """
    Return a function that takes a line of text and returns the number of
    characters before a match with `regex` is found. If no match is found, 0
    is returned.

    Args:
    ----
        regex: the regular expression to match.

    Returns:
    -------
        a function that takes a line of text and returns the number of
        characters before a match with `regex` is found.
    """

    def len_to_match(line: str) -> int:
        match = re.search(regex, line)
        return match.start() if match else 0

    return len_to_match
