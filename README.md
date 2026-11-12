# Student Result Management System

A menu-driven Python application that lets a school register students, record
subject scores, calculate totals/averages/grades, generate reports and keep
all data in a JSON file.

## Features
- Add, view, search, update and delete students
- Record and update scores for 5 subjects (Mathematics, English Language, Physics, Chemistry, Biology)
- Automatic total, average and grade (A-F)
- Individual report card
- Results list sorted by average (high to low) or by name
- Class statistics (class average, best/weakest student, highest/lowest score)
- Save a text report to the `reports/` folder
- Data saved to `data/students.json` and loaded on start-up (missing file handled)

## Grading scale
| Average | Grade |
|---|---|
| 70 - 100 | A |
| 60 - 69 | B |
| 50 - 59 | C |
| 45 - 49 | D |
| below 45 | F |

## How to run
Requires Python 3.8 or newer. No extra packages needed.

```
python main.py
```

## Project structure
```
student_result_system/
├── main.py       # entry point, menu and input validation
├── student.py    # Student class
├── results.py    # subjects, score validation, grading
├── storage.py    # load/save JSON
├── reports.py    # report card, tables, statistics, file export
├── data/
│   └── students.json   # created automatically
└── README.md
```

## Python concepts used
Variables and type conversion, if/elif/else, for/while loops, lists, tuples,
dictionaries, functions, sorting (`sorted` with `key`), exception handling
(try/except/else/finally), JSON file handling, modules, OOP (`Student` class),
`datetime`, `os`, `json`, `re` (regex validation of Student ID).
