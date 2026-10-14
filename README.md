# Lab 5: Static Code Analysis

## Pharmacy Manager — Python Project

### 1. Objective

The objective of this lab is to improve the quality, readability, maintainability, and security of a Python program using static code analysis tools. The tools used are Pylint, Bandit, and Flake8.

### 2. Project Overview

The Pharmacy Manager application demonstrates basic pharmacy operations, including:

- Adding and dispensing medicines
- Checking medicine quantities and expiry dates
- Calculating bills and medicine dosages
- Generating patient identifiers and prescription numbers
- Saving and loading pharmacy stock
- Generating dispensing labels
- Pharmacist login verification
- Displaying pharmacy stock reports

### 3. Tools Used

| Tool   | Purpose                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------ |
| Pylint | Detects code-quality problems, naming issues, missing documentation, and potential design flaws. |
| Bandit | Detects potentially insecure Python coding patterns.                                             |
| Flake8 | Checks Python formatting and PEP 8 style violations.                                             |

**Environment:** Python 3.13.7

**Main file:** `pharmacy_manager.py`

### 4. Commands Used

Run these commands from the project directory.

```cmd
python pharmacy_manager.py
python -m pylint pharmacy_manager.py
python -m bandit pharmacy_manager.py
python -m flake8 pharmacy_manager.py
```

To save the reports to text files:

```cmd
python -m pylint pharmacy_manager.py > pylint_report.txt
python -m bandit pharmacy_manager.py > bandit_report.txt
python -m flake8 pharmacy_manager.py > flake8_report.txt
```

### 5. Before-and-After Analysis Results

| Tool   | Initial result                           | Final result           |
| ------ | ---------------------------------------- | ---------------------- |
| Pylint | 4.83/10                                  | 10.00/10               |
| Bandit | Multiple security findings               | No issues identified   |
| Flake8 | Multiple formatting and style violations | No reported violations |

The initial reports identified security concerns, unused imports, long lines, incorrect spacing, naming inconsistencies, and other code-quality problems.

The final reports indicate that the program meets the lab's stated target of a Pylint score above 9.5, with no reported Bandit or Flake8 findings.

### 6. Issue Identification and Fixes

| No. | Issue identified                            | Fix applied                                                              |
| --- | ------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | Use of `eval()` for dosage calculation      | Replaced arbitrary expression evaluation with restricted input handling. |
| 2   | Use of MD5 hashing                          | Changed patient identifier generation to SHA-256.                        |
| 3   | Use of `random` for prescription numbers    | Used the `secrets` module for less predictable identifiers.              |
| 4   | Use of pickle for stock persistence         | Replaced pickle-based storage with JSON.                                 |
| 5   | Shell command execution using `os.system()` | Replaced shell execution with normal Python output.                      |
| 6   | Hard-coded password                         | Moved password configuration to an environment variable.                 |
| 7   | Unused imports                              | Removed unnecessary imports.                                             |
| 8   | Incorrect blank-line spacing                | Corrected spacing to follow PEP 8.                                       |
| 9   | Lines exceeding the length limit            | Wrapped long statements across multiple lines.                           |
| 10  | Bare exception handling                     | Used more appropriate exception handling.                                |
| 11  | Missing module and function docstrings      | Added documentation where required.                                      |
| 12  | Inconsistent function naming                | Changed function names to snake_case.                                    |
| 13  | Mutable default argument                    | Used `None` and initialized the value inside the function.               |

### 7. Final Program Verification

The final execution of `pharmacy_manager.py` confirmed that the program runs and displays pharmacy stock information.

The output demonstrated:

- Handling of an attempt to dispense an unregistered medicine.
- Updated Paracetamol stock of 170 units.
- Expiry-status checking for Amoxicillin.
- Bill calculation of Rs. 45.0.
- Dosage calculation of 500.0 mg/day.
- Generation of a patient identifier and prescription number.
- Dispensing-label output and the pharmacy stock report.

**Note:** The displayed login result was `False` because the `DB_PASSWORD` environment variable was not set in that terminal session. This is separate from the static-analysis results.

### 8. Reflection

**What is the purpose of static code analysis?**

Static code analysis examines source code without requiring the program to be executed. It helps identify potential security vulnerabilities, style violations, and maintainability problems early in development.

**What did the three tools help identify?**

Pylint highlighted code-quality and maintainability issues. Flake8 identified formatting and PEP 8 violations. Bandit detected potentially unsafe patterns involving expression evaluation, hashing, random number generation, serialization, and shell execution.

**What did I learn from this lab?**

I learned that a program can run correctly and still contain security and maintainability problems. Using multiple static analysis tools provides a more comprehensive review of code. Re-running the tools after applying fixes also helps verify that the reported issues have been addressed.

### 9. Git Commit History

The lab requires three commits covering changes related to the analysis tools. Use meaningful commit messages that reflect the actual changes made.

Example commit messages:

```text
Fix security findings reported by Bandit
Resolve Pylint code quality warnings
Fix Flake8 formatting violations
```

Verify the actual commit history with:

```cmd
git log --oneline
```


**Conclusion:** The Pharmacy Manager program was reviewed using Pylint, Bandit, and Flake8. The final reported results were a Pylint score of 10.00/10, zero Bandit findings, and no reported Flake8 violations. These results demonstrate improvements in code quality, formatting, and security checks.
