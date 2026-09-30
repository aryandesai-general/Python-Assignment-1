"""Q1: Campus Merit Analyzer using lists, tuples and dictionaries.

Input:
n k m
enrollment name semester cpi mark1 ... markm
"""
from collections import defaultdict
import sys


def main():
    first = sys.stdin.readline().split()
    if len(first) != 3:
        print("Invalid input: expected n k m.")
        return

    try:
        n, k, m = map(int, first)
        if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
            raise ValueError
    except ValueError:
        print("Invalid input: n, k or m is outside the allowed range.")
        return

    students = []
    by_semester = defaultdict(list)
    subject_top = [(-1, []) for _ in range(m)]

    for _ in range(n):
        parts = sys.stdin.readline().split()
        if len(parts) != 4 + m:
            print("Invalid student record.")
            return
        enrollment, name = parts[0], parts[1]
        try:
            semester = int(parts[2])
            cpi = float(parts[3])
            marks = tuple(map(int, parts[4:]))
            if not 1 <= semester <= 8 or not 0 <= cpi <= 10:
                raise ValueError
            if any(not 0 <= mark <= 100 for mark in marks):
                raise ValueError
        except ValueError:
            print("Invalid student data.")
            return

        record = {
            "enrollment": enrollment,
            "name": name,
            "semester": semester,
            "cpi": cpi,
            "marks": marks,
            "average": sum(marks) / m,
        }
        students.append(record)
        by_semester[semester].append(record)

    # Higher CPI, then higher average, then smaller enrollment number.
    for semester in sorted(by_semester):
        ranked = sorted(
            by_semester[semester],
            key=lambda s: (-s["cpi"], -s["average"], s["enrollment"])
        )
        top = ranked[:k]
        print(f"Semester {semester}:", *(s["enrollment"] for s in top))

    # Print every student tied for the highest mark in each subject.
    for subject in range(m):
        highest = max(s["marks"][subject] for s in students)
        toppers = sorted(
            s["enrollment"] for s in students
            if s["marks"][subject] == highest
        )
        print(f"S{subject + 1}:", *toppers)


if __name__ == "__main__":
    main()
