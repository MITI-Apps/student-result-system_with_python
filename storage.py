"""storage.py - load and save student data as JSON."""
import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Return {student_id: Student}. Returns {} if the file is missing/corrupt."""
    students = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found yet - starting with an empty record.")
    except json.JSONDecodeError:
        print("Data file is damaged - starting with an empty record.")
    else:
        for item in raw:
            student = Student.from_dict(item)
            students[student.student_id] = student
        print(f"Loaded {len(students)} student(s).")
    finally:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return students


def save_students(students, path=DATA_FILE):
    """Write all students to the JSON file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as err:
        print(f"Could not save data: {err}")
        return False
    return True
