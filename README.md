# Programming with Python — Assignment 1

**Course:** Programming with Python (202044504)  
**Program:** B.Tech. Information Technology — Semester V

This repository contains Python 3 solutions for the ten questions in Assignment 1.

## Questions

| File | Problem |
|---|---|
| `Q1_Campus_Merit_Analyzer.py` | Campus Merit Analyzer using compound data structures |
| `Q2_Optimized_Password_Audit.py` | Password audit with pattern constraints |
| `Q3_Recursive_Expression_Engine.py` | Recursive expression evaluator with memoization |
| `Q4_Exception_Safe_CSV_Transaction_Splitter.py` | CSV transaction validation and splitting |
| `Q5_OOP_Bank_Settlement_System.py` | Object-oriented bank settlement and batch rollback |
| `Q6_Python_Module_Dependency_Resolver.py` | Module dependency ordering and cycle detection |
| `Q7_Interactive_Formula_Validator.py` | Interactive calculator with custom exceptions |
| `Q8_Compressed_Log_Index.py` | Pickle-based log index and ZIP archive |
| `Q9_Threaded_Job_Scheduler.py` | Multi-worker job scheduling simulation |
| `Q10_Tkinter_Assignment_Tracker.py` | Tkinter assignment tracker with JSON and CSV |

## Requirements

- Python 3.10 or newer
- Q1–Q9 use the Python standard library.
- Q10 uses `tkinter`, which is included with many Python installations. On some Linux systems, it may need to be installed separately.

No third-party Python packages are required.

## Run a program

Open a terminal in this folder and run the relevant file:

```bash
python3 Q1_Campus_Merit_Analyzer.py
```

Most console programs read input from standard input. For example:

```bash
python3 Q1_Campus_Merit_Analyzer.py < input.txt
```

Q4 asks for a CSV file path. Q7 accepts formulas until `quit` is entered. Q8 accepts a `BUILD` or `SEARCH` command through standard input. Q10 launches a desktop GUI.

## Important notes

- Read each program before submitting it, and test it with the sample input and additional edge cases.
- Q4 creates `credit.csv`, `debit.csv`, and `error.csv` in the current working directory.
- Q5 rolls back the active batch if an operation in that batch fails.
- Q8 creates a `.pkl` index beside the requested ZIP archive.
- Q10 saves records to `assignments.json` and exports `assignment_report.csv`.
- In Q9, the assignment does not specify a total shared-resource capacity. The simulation therefore schedules against worker availability and retains the `resources` field as input metadata.

## Suggested GitHub upload

1. Create a new GitHub repository, for example `python-assignment-1`.
2. Upload all ten `.py` files and this `README.md`.
3. Add screenshots or sample input/output files if your faculty asks for test evidence.
4. Do not upload private student data or real transaction records.
