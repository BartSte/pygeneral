import logging
import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from sys import stdin

from pygeneral.sort import lensort

_DESCRIPTION = """
Sort lines of text based on the number of characters before a regular
expression match is found. Lines with the least number of characters move to
the top, and lines with the most number of characters move to the bottom. The
text to be sorted is read from stdin and the sorted text is written to
stdout. For example, if we have the following input:

    abc = 1
    x = 2
    yy = 3

Then if our regular expression is `=', the output would be:

    x = 2
    yy = 3
    abc = 1

If our input was located in a file called `input.txt', we could use the
following command to sort the text when using bash:

    lensort '=' < input.txt
"""


def main():
    """Entrypoint"""
    try:
        _main()
    except Exception as error:
        logging.critical(error)
        sys.exit(1)


def _main():
    """Entrypoint without error handling."""
    parser: ArgumentParser = _make_parser()
    args: Namespace = parser.parse_args()
    logging.basicConfig(level=parser.parse_args().loglevel)

    text: str = _read(args.file) if args.file else stdin.read()
    logging.debug("Input text: %s", text)

    sorted_text: str = lensort(text, args.regex)
    logging.debug("Sorted text: %s", sorted_text)

    print(sorted_text)


def _make_parser() -> ArgumentParser:
    """
    Create an argument parser for the lensort command.

    Returns:
    -------
        ArgumentParser: an argument parser for the lensort command.

    """
    parser = ArgumentParser(
        prog="sort_variable_length",
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "regex", type=str, help="The regular expression to sort the text by."
    )

    parser.add_argument(
        "-l",
        "--loglevel",
        type=str,
        default="INFO",
        help="Set the log level for the program.",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help=(
            "The file to read the text from. If not provided, text is read "
            "from stdin."
        ),
    )

    return parser


def _read(path: str) -> str:
    """
    Read the text from a file.

    Args:
    ----
        path: the path to the file.

    Returns:
    -------
        the text from the file.

    """
    with open(path, "r") as file:
        return file.read()
