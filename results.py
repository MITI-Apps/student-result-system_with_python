"""results.py - score validation and grading logic."""

SUBJECTS = ["Mathematics", "English Language", "Physics", "Chemistry", "Biology"]

# (minimum average, grade) checked from the top down
GRADE_SCALE = [(70, "A"), (60, "B"), (50, "C"), (45, "D")]


def validate_score(value):
    """Convert text to a float between 0 and 100, or raise ValueError."""
    score = float(value)              # raises ValueError for non-numbers
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def get_grade(average):
    for minimum, grade in GRADE_SCALE:
        if average >= minimum:
            return grade
    return "F"


def remark(grade):
    remarks = {"A": "Excellent", "B": "Very Good", "C": "Good",
               "D": "Fair", "F": "Fail"}
    return remarks[grade]
