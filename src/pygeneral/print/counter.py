from typing import override

from pygeneral.print.abstract import AbstractAnimation


class Counter(AbstractAnimation):
    """
    A simple counter that writes progress to standard output on a single line.

    Attributes:
        index: The current count.
        goal: The optional goal or upper limit for the counter.
        prefix: An optional prefix string to display before the counter.
        suffix: An optional suffix string to display after the counter.
    """

    _value: int | float
    goal: int | None
    prefix: str
    suffix: str

    def __init__(
        self,
        *,
        value: int = 0,
        goal: int | None = None,
        prefix: str = "",
        suffix: str = "",
    ) -> None:
        """
        Initialize the StdoutCounter.

        Args:
            value: The starting count (default 0).
            goal: The optional end goal for the counter.
            prefix: Text to display before the count.
            suffix: Text to display after the count.
        """
        super().__init__(value=value)
        self.goal = goal
        self.prefix = prefix
        self.suffix = suffix

    @override
    def make_message(self) -> str:
        """
        Build the progress message for display on stdout.

        Returns:
            A string containing the prefix, current count, and suffix
            (including a carriage return at the beginning).
        """
        count_str = self.make_count()
        return f"\r{self.prefix}{count_str}{self.suffix}"

    def make_count(self) -> str:
        """
        Create a human-readable representation of the current count
        and goal (if provided).

        Returns:
            A string with either just the current count, or `current/goal`.
        """
        if self.goal is None:
            return str(self._value)
        return f"{self._value}/{self.goal}"
