"""main.py - entry point and menu for the Student Result Management System."""
import re
from datetime import datetime

import reports
from results import SUBJECTS, validate_score
from storage import load_students, save_students
from student import Student

ID_PATTERN = re.compile(r"^[A-Za-z]{2,5}[-/]?\d{2,5}$")   # e.g. STU001, ABU/2024


# ---------------------------------------------------------------- input helpers
def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


def ask_student_id(prompt="Student ID (e.g. STU001): "):
    while True:
        value = input(prompt).strip().upper()
        if ID_PATTERN.match(value):
            return value
        print("  Invalid ID. Use letters then digits, e.g. STU001 or ABU/2024.")


def ask_gender():
    while True:
        value = input("Gender (M/F): ").strip().upper()
        if value in ("M", "F"):
            return "Male" if value == "M" else "Female"
        print("  Enter M or F.")


def ask_dob():
    while True:
        value = input("Date of birth (YYYY-MM-DD): ").strip()
        try:
            born = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("  Invalid date. Use the format YYYY-MM-DD.")
        else:
            if born > datetime.now():
                print("  Date of birth cannot be in the future.")
            else:
                return value


def ask_score(subject, current=None):
    hint = f" [Enter keeps {current}]" if current is not None else ""
    while True:
        text = input(f"  {subject} (0-100){hint}: ").strip()
        if text == "" and current is not None:
            return current
        try:
            return validate_score(text)
        except ValueError as err:
            print(f"  Invalid: {err if 'between' in str(err) else 'enter a number.'}")


def find_student(students, student_id=None):
    sid = student_id or ask_student_id("Enter student ID: ")
    student = students.get(sid)
    if student is None:
        print("  No student with that ID.")
    return student


# ---------------------------------------------------------------- menu actions
def add_student(students):
    sid = ask_student_id()
    if sid in students:
        print("  That ID is already registered.")
        return
    name = ask_text("Full name: ")
    cls = ask_text("Class/Form: ")
    students[sid] = Student(sid, name.title(), cls.upper(), ask_gender(), ask_dob())
    save_students(students)
    print(f"  Student {sid} added.")


def view_students(students):
    if not students:
        print("  No students registered yet.")
        return
    for s in reports.sort_students(students, "name"):
        print(" ", s)


def search_students(students):
    term = ask_text("Search by ID or name: ").lower()
    matches = [s for s in students.values()
               if term == s.student_id.lower() or term in s.name.lower()]
    if not matches:
        print("  No match found.")
    for s in matches:
        print(" ", s)


def update_student(students):
    s = find_student(students)
    if s is None:
        return
    print("  Leave a field blank to keep its current value.")
    name = input(f"Name [{s.name}]: ").strip()
    cls = input(f"Class [{s.student_class}]: ").strip()
    gender = input(f"Gender M/F [{s.gender}]: ").strip().upper()
    dob = input(f"DOB YYYY-MM-DD [{s.dob}]: ").strip()
    if name:
        s.name = name.title()
    if cls:
        s.student_class = cls.upper()
    if gender in ("M", "F"):
        s.gender = "Male" if gender == "M" else "Female"
    if dob:
        try:
            datetime.strptime(dob, "%Y-%m-%d")
            s.dob = dob
        except ValueError:
            print("  Invalid date ignored; DOB unchanged.")
    save_students(students)
    print("  Student updated.")


def delete_student(students):
    s = find_student(students)
    if s is None:
        return
    if input(f"Delete {s.name}? (y/n): ").strip().lower() == "y":
        del students[s.student_id]
        save_students(students)
        print("  Student deleted.")
    else:
        print("  Cancelled.")


def record_scores(students):
    s = find_student(students)
    if s is None:
        return
    print(f"  Scores for {s.name}:")
    new_scores = {sub: ask_score(sub, s.scores.get(sub)) for sub in SUBJECTS}
    s.set_scores(new_scores)
    save_students(students)
    print("  Scores saved.")


def show_report_card(students):
    s = find_student(students)
    if s:
        print(reports.report_card(s))


def show_results(students):
    if not students:
        print("  No students registered yet.")
        return
    choice = input("Sort by (1) average, high to low  (2) name: ").strip()
    print(reports.result_table(students, "name" if choice == "2" else "average"))


def show_statistics(students):
    print(reports.statistics_text(students))


def export_report(students):
    if not students:
        print("  Nothing to report yet.")
        return
    print(f"  Report saved to: {reports.save_report(students)}")


# ---------------------------------------------------------------- main loop
MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student              6. Record / update scores
 2. View all students        7. Show report card
 3. Search student           8. List results (sorted)
 4. Update student info      9. Class statistics
 5. Delete student          10. Save class report to file
 0. Exit
"""

ACTIONS = {
    "1": add_student, "2": view_students, "3": search_students,
    "4": update_student, "5": delete_student, "6": record_scores,
    "7": show_report_card, "8": show_results, "9": show_statistics,
    "10": export_report,
}


def main():
    students = load_students()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save_students(students)
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action(students)
        else:
            print("  Invalid option, try again.")


if __name__ == "__main__":
    main()
