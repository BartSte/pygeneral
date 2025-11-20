# Changelog - pygeneral

This document describes the changes that were made to the software for each
version. The changes are described concisely, to make it comprehensible for the
user. A change is always categorized based on the following types:

- Bug: a fault in the software is fixed.
- Feature: a functionality is added to the program.
- Improvement: a functionality in the software is improved.
- Task: a change is made to the repository that has no effect on the source
  code.
- Breaking: a change is made that is not backwards compatible.

## 1.0

### Breaking

- The animations require `show` to be called to draw upon value change.

### Features

- Added `multiple.py` for handling multiple animations simultaneously.
- Added streaming subprocess stdout/stderr to multiple sinks.

### Bug

- Decreased python version to 3.12 as 3.13 is not the default for ubuntu yet.

## 0.2

### Features

- Added rotator.py
- Added path.py

### Bug

- Show an hide the cursor during animations

## 0.1

### Features

- Added progress bar

## 0.0

### Features

- Added `lensort`, `is_root`, and `StdoutCounter` classes.
