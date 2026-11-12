"""reports.py - report cards, result lists, statistics and file export."""
import os
from datetime import datetime

from results import get_grade, remark

LINE = "=" * 78


def sort_students(students, by="average"):
    """Return a sorted list: by 'average' (high to low) or by 'name'."""
    items = list(students.values())
    if by == "name":
        return sorted(items, key=lambda s: s.name.lower())
    return sorted(items, key=lambda s: s.average, reverse=True)


def result_table(students, by="average"):
    """Text table of every student with total, average and grade."""
    rows = [LINE,
            f"{'ID':<10}{'Name':<26}{'Class':<10}{'Total':>8}{'Average':>10}{'Grade':>8}",
            LINE]
    for position, s in enumerate(sort_students(students, by), start=1):
        if s.has_scores:
            rows.append(f"{s.student_id:<10}{s.name:<26}{s.student_class:<10}"
                        f"{s.total:>8.1f}{s.average:>10.2f}{get_grade(s.average):>8}")
        else:
            rows.append(f"{s.student_id:<10}{s.name:<26}{s.student_class:<10}"
                        f"{'-':>8}{'-':>10}{'-':>8}")
    rows.append(LINE)
    return "\n".join(rows)


def report_card(student):
    """Text report card for one student."""
    lines = [LINE, "STUDENT REPORT CARD".center(78), LINE,
             f"Name   : {student.name}",
             f"ID     : {student.student_id}",
             f"Class  : {student.student_class}",
             f"Gender : {student.gender}",
             f"DOB    : {student.dob}",
             "-" * 78,
             f"{'Subject':<30}{'Score':>10}"]
    if not student.has_scores:
        lines.append("No scores recorded yet.")
    else:
        for subject, score in student.scores.items():
            lines.append(f"{subject:<30}{score:>10.1f}")
        grade = get_grade(student.average)
        lines += ["-" * 78,
                  f"{'Total':<30}{student.total:>10.1f}",
                  f"{'Average':<30}{student.average:>10.2f}",
                  f"{'Grade':<30}{grade:>10}  ({remark(grade)})",
                  f"Result entered: {student.result_date}"]
    lines.append(LINE)
    return "\n".join(lines)


def class_statistics(students):
    """Return a dict of class statistics, or None if no scores exist."""
    scored = [s for s in students.values() if s.has_scores]
    if not scored:
        return None
    best = max(scored, key=lambda s: s.average)
    worst = min(scored, key=lambda s: s.average)
    all_scores = [(score, s.name, subject)
                  for s in scored for subject, score in s.scores.items()]
    return {
        "count": len(scored),
        "class_average": sum(s.average for s in scored) / len(scored),
        "top_student": best,
        "bottom_student": worst,
        "highest_score": max(all_scores),
        "lowest_score": min(all_scores),
    }


def statistics_text(students):
    stats = class_statistics(students)
    if stats is None:
        return "No scores recorded yet, so there are no statistics."
    hs, ls = stats["highest_score"], stats["lowest_score"]
    return "\n".join([
        "CLASS STATISTICS", "-" * 40,
        f"Students with results : {stats['count']}",
        f"Class average         : {stats['class_average']:.2f}",
        f"Best student          : {stats['top_student'].name} ({stats['top_student'].average:.2f})",
        f"Weakest student       : {stats['bottom_student'].name} ({stats['bottom_student'].average:.2f})",
        f"Highest single score  : {hs[0]:.1f} - {hs[1]} ({hs[2]})",
        f"Lowest single score   : {ls[0]:.1f} - {ls[1]} ({ls[2]})",
    ])


def save_report(students, folder="reports"):
    """Write the full class report to a timestamped .txt file; return its path."""
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"class_report_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("CLASS RESULT REPORT\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(result_table(students, "average") + "\n\n")
        f.write(statistics_text(students) + "\n")
    return path
