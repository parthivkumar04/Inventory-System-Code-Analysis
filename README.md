# Lab 5 >>> Inventory System Static Code Analysis Report

This document outlines the findings and comprehensive fixes applied to the original `inventory_system.py` file using Pylint, Bandit and Flake8, along with the required reflection's answers.

## Issue Table


| Issue | Tool/Type | Line(s) (Original) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **I. CRITICAL ISSUES (Security & Correctness)** | | | | |
| **Insecure use of `eval`** | Bandit (B307) / Pylint (W0123) | 59 | Use of the possibly insecure `eval()` function, which executes arbitrary code. | Removed the line entirely. |
| **Mutable default arg** | Pylint (W0102) | 8 | Dangerous default value `logs=[]` is shared across all function calls. | Changed the default to `None` and initialized the list conditionally. |
| **Bare `except`** | Pylint (W0702) / Bandit (B110) / Flake8 (E722) | 19 | Using a bare `except:` clause catches all exceptions, masking critical errors. | Replaced with specific exception: `except KeyError:`. |
| **Untyped Input** | Runtime Error | 51 | The `addItem` call with `"ten"` caused a `TypeError` due to lack of validation. | Added `isinstance` check for `qty` to validate input type. |
| **II. BEST PRACTICE & RESOURCE MANAGEMENT** | | | | |
| **Resource Leaks** | Pylint (R1732) | 26, 32 | Opening files without the `with` statement, risking file handles not being closed reliably. | Implemented the **`with open(...) as f:`** context manager. |
| **Unspecified Encoding** | Pylint (W1514) | 26, 32 | Using `open` without explicitly specifying `encoding`. | Explicitly set **`encoding='utf-8'`** in all `open` calls. |
| **Global Statement** | Pylint (W0603) | 27 | Using the `global` statement makes data flow confusing. | **Refactored entire script** into an `InventorySystem` class, eliminating the need for `global`. |
| **III. STYLE & READABILITY (PEP 8)** | | | | |
| **Non-snake_Case Name** | Pylint (C0103) | 8, 14, 22, 25, 31, 36, 41, 48 | Function names do not conform to PEP 8's `snake_case`. | Renamed all functions and methods to use `snake_case`. |
| **Missing Docstrings** | Pylint (C0114, C0116) | 1, 8, 14, 22, 25, 31, 36, 41, 48 | Missing module docstring (line 1) and all 8 function docstrings. | Added concise docstrings to the module, class, and every method. |
| **Unused Import** | Pylint (W0611) / Flake8 (F401) | 2 | The `logging` module was imported but never used. | Removed the line `import logging`. |
| **F-string Use** | Pylint (C0209) | 12 | Using old C-style `%` string formatting. | Replaced with modern, readable **f-strings**. |
| **Spacing/Style** | Flake8 (E302, E305) | Various | Incorrect number of blank lines around definitions. | Adjusted spacing to enforce 2 blank lines between top-level definitions and 1 blank line between class methods. |
| **Line Too Long** | Flake8 (E501) | Various | Lines exceeded the 79-character limit. | Broke long strings and `print` statements into multiple lines. |

---

## Reflection Q & A

### Which issues were the easiest to fix and which were the hardest? Why?
The easiest issues were the **style violations (Flake8)**, such as unused imports (`F401` for `logging`) and incorrect function spacing (`E302/E305`). These required minimal effort, only deleting a line or adding a blank line. The **`eval()` function call (Bandit B307)** was also easy, as it simply needed to be removed eliminating a critical security risk.

**Hardest to Fix:**
The hardest issue was **refactoring to eliminate the global state (`W0603`)**. To fully resolve this architectural warning, we had to move the entire script into an `InventorySystem` class. This required redesigning every function to be a method (`self.add_item`), updating variable access (`stock_data` became `self.stock_data`) and modifying the `main()` execution loop. This was the most complex and time-consuming change.

### Did the static analysis tools report any false positives? If so, describe one example.
Yes, the tools reported one issue that could be considered a functional false positive: **The bare `except` statement (`W0702`) in `removeItem`**. The tool was correct about the poor practice, but the fix required specifying the intended exception (`except KeyError:`) rather than fixing a logical bug.

### How would you integrate static analysis tools into your actual software development workflow? Consider continuous integration (CI) or local development practices.
I would use local **pre-commit hooks** for instant feedback (Flake8, Pylint) and **CI pipelines** (Bandit, Pylint, Flake8) to enforce quality standards on every pull request.

### What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
Improvements included increased **Robustness** (fixing mutable defaults), better **Security** (removing `eval`), enhanced **Readability** (snake\_case/f-strings) and higher **Maintainability** (class refactoring).
