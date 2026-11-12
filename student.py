"""student.py - the Student class."""
from datetime import datetime


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, student_class, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id
        self.name = name
        self.student_class = student_class
        self.gender = gender
        self.dob = dob                    # stored as "YYYY-MM-DD"
        self.scores = scores or {}        # {"Mathematics": 75.0, ...}
        self.result_date = result_date    # when scores were last entered

    # ---- scores -------------------------------------------------------
    def set_scores(self, scores):
        """Replace scores and stamp the date/time they were entered."""
        self.scores = dict(scores)
        self.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def has_scores(self):
        return len(self.scores) > 0

    @property
    def total(self):
        return sum(self.scores.values())

    @property
    def average(self):
        return self.total / len(self.scores) if self.scores else 0.0

    # ---- saving / loading --------------------------------------------
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "student_class": self.student_class,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["name"], data["student_class"],
            data["gender"], data["dob"],
            data.get("scores", {}), data.get("result_date"),
        )

    def __str__(self):
        return f"{self.student_id} | {self.name} | {self.student_class} | {self.gender} | {self.dob}"
