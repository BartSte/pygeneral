# README - pygeneral

A collection of general-purpose Python utilities.

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

- **`ProgressBar`** is a simple progress bar that can be used in the console.
- **`StdoutCounter`** provides a straightforward way to show progress in the console, incrementally updating a single line.
- **`is_root`** helps you check if the current user has root (on Linux/Unix) or administrator (on Windows) privileges.
- **`lensort`** sorts lines based on their distance to a match of a specified regular expression.

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

## Usage

You can import the classes and functions from `pygeneral` as you normally would
with in a Python script. Additionally, some of the utilities are also available
as command-line tools. As is explained below.

### Lensort

After installation, you will have the `lensort` command available:

```bash
lensort [OPTIONS] <REGEX>
```

#### Example

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

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
See the [LICENSE](LICENSE) file for details.
