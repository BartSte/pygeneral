# README - pygeneral

A collection of general-purpose Python utilities, including:

- **`lensort`**: Sort lines of text based on the number of characters before a regular expression match.
- **`StdoutCounter`**: A simple progress counter that writes progress to `stdout`.
- **`is_root`**: Check if the script is run with root (administrator) privileges.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Command-Line Usage](#command-line-usage)
4. [Python Usage](#python-usage)
   - [Sorting with `lensort`](#sorting-with-lensort)
   - [Using `StdoutCounter`](#using-stdoutcounter)
   - [Checking Root Privileges with `is_root`](#checking-root-privileges-with-is_root)
5. [Project Structure](#project-structure)
6. [License](#license)

---

## Overview

`pygeneral` is a set of small Python utilities that can simplify common tasks.

- **`lensort`** sorts lines based on their distance to a match of a specified regular expression.
  - Lines are first sorted by length, then by the position of the regex match (lines with no match come first).
- **`StdoutCounter`** provides a straightforward way to show progress in the console, incrementally updating a single line.
- **`is_root`** helps you check if the current user has root (on Linux/Unix) or administrator (on Windows) privileges.

---

## Installation

```bash
pip install pygeneral
```

Or, for development:

```bash
# (1) Clone the repository
git clone https://github.com/BartSte/pygeneral.git
cd pygeneral
pip install -e ".[dev]"
```

---

## Command-Line Usage

After installation, you will have the `lensort` command available:

```bash
lensort [OPTIONS] <REGEX>
```

### Example

Suppose you have a file named `input.txt`:

```
abc = 1
x = 2
yy = 3
```

If you run:

```bash
lensort '=' -f input.txt
```

The output will be:

```
x = 2
yy = 3
abc = 1
```

Explanation:

- It sorts lines by the number of characters before the `=` match.
- `x = 2` has 1 character before `=`.
- `yy = 3` has 2 characters before `=`.
- `abc = 1` has 3 characters before `=`.

You can also pipe content directly to `lensort`, for example:

```bash
cat input.txt | lensort '='
```

**Options:**

- `-l, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}`: Set the logging level (default: `INFO`).
- `-f, --file <FILE>`: Read text from a file instead of `stdin`.

---

## Python Usage

### Using `StdoutCounter`

To display incremental progress on the console:

```python
import time
from pygeneral.print import StdoutCounter

counter = StdoutCounter(
    index=0,
    goal=5,
    prefix="Processing: ",
    suffix=" items complete"
)

for _ in range(5):
    time.sleep(1)  # Simulating some work
    counter.increment()
```

This will produce a line on the console that updates from `0/5` to `5/5`.

### Checking Root Privileges with `is_root`

```python
from pygeneral.permission import is_root

if is_root():
    print("Running as root!")
else:
    print("Not running as root.")
```

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
See the [LICENSE](LICENSE) file for details.
