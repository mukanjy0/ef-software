from __future__ import annotations

from dataclasses import dataclass
from typing import List

MAX_EVALUATIONS = 10
MIN_GRADE = 0.0
MAX_GRADE = 20.0
MAX_FINAL_GRADE = 20.0
ATTENDANCE_THRESHOLD = 0.7  # 70%
EXTRA_POINTS_VALUE = 1.0
MIN_WEIGHT_PERCENTAGE = 1
MAX_WEIGHT_PERCENTAGE = 100
TOTAL_WEIGHT_PERCENTAGE = 100


@dataclass(frozen=True)
class Evaluation:
    mark: float
    weight_percentage: int

    def __post_init__(self) -> None:
        if not (MIN_GRADE <= self.mark <= MAX_GRADE):
            raise ValueError("Mark must be between 0 and 20.")
        if not (
            MIN_WEIGHT_PERCENTAGE
            <= self.weight_percentage
            <= MAX_WEIGHT_PERCENTAGE
        ):
            raise ValueError(
                f"Weight percentage must be between "
                f"{MIN_WEIGHT_PERCENTAGE} and {MAX_WEIGHT_PERCENTAGE}."
            )


def handle_minimum_attendance(
    grade: float,
    attendance_ratio: float,
    threshold: float = ATTENDANCE_THRESHOLD,
) -> float:
    if not 0.0 <= attendance_ratio <= 1.0:
        raise ValueError("Attendance ratio must be between 0 and 1.")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Threshold must be between 0 and 1.")
    if attendance_ratio < threshold:
        return 0.0
    return grade


def handle_extra_points(
    grade: float,
    extra_points_enabled: bool,
    extra_points: float = EXTRA_POINTS_VALUE,
) -> float:
    if extra_points < 0.0:
        raise ValueError("Extra points must be non-negative.")
    if not extra_points_enabled:
        return grade
    return min(MAX_FINAL_GRADE, grade + extra_points)


class GradeCalculator:
    def __init__(self, evaluations: List[Evaluation]) -> None:
        if len(evaluations) == 0:
            raise ValueError("At least one evaluation is required.")
        if len(evaluations) > MAX_EVALUATIONS:
            raise ValueError("Maximum number of evaluations exceeded.")

        total_weight = sum(e.weight_percentage for e in evaluations)
        if total_weight != TOTAL_WEIGHT_PERCENTAGE:
            raise ValueError("The sum of weight percentages must be 100.")

        self._evaluations = evaluations

    def calculate_final_grade(
        self,
        attendance_ratio: float,
        extra_points_enabled: bool,
    ) -> float:
        base_grade = self._calculate_weighted_average()

        after_attendance = handle_minimum_attendance(
            base_grade,
            attendance_ratio,
            ATTENDANCE_THRESHOLD,
        )

        # If the student did not reach the minimum attendance,
        # the grade is 0 and extra points are not applied.
        if after_attendance == 0.0 and attendance_ratio < ATTENDANCE_THRESHOLD:
            return 0.0

        after_extra = handle_extra_points(
            after_attendance,
            extra_points_enabled,
            EXTRA_POINTS_VALUE,
        )
        return min(MAX_FINAL_GRADE, after_extra)

    def _calculate_weighted_average(self) -> float:
        total = sum(
            e.mark * e.weight_percentage for e in self._evaluations
        )
        return total / float(TOTAL_WEIGHT_PERCENTAGE)


def _read_float(prompt: str) -> float:
    while True:
        raw_value = input(prompt).strip()
        try:
            return float(raw_value)
        except ValueError:
            print("Please enter a valid number.")


def _read_int(prompt: str) -> int:
    while True:
        raw_value = input(prompt).strip()
        try:
            return int(raw_value)
        except ValueError:
            print("Please enter a valid integer.")


def _read_yes_no(prompt: str) -> bool:
    while True:
        raw_value = input(prompt + " (y/n): ").strip().lower()
        if raw_value in ("y", "yes"):
            return True
        if raw_value in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def _read_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a non-empty value.")


def _read_evaluation_count() -> int:
    while True:
        count = _read_int("How many evaluations does the student have? ")
        if count <= 0:
            print("There must be at least one evaluation.")
            continue
        if count > MAX_EVALUATIONS:
            print(
                f"Maximum number of evaluations is {MAX_EVALUATIONS}. "
                f"Please enter a valid number."
            )
            continue
        return count


def _read_evaluations() -> List[Evaluation]:
    while True:
        count = _read_evaluation_count()
        evaluations: List[Evaluation] = []

        for index in range(1, count + 1):
            while True:
                print(f"\nEvaluation {index}")
                mark = _read_float("  Mark (0–20): ")
                weight_percentage = _read_int(
                    "  Weight percentage (1–100, e.g. 30 for 30%): "
                )
                try:
                    evaluation = Evaluation(
                        mark=mark,
                        weight_percentage=weight_percentage,
                    )
                except ValueError as error:
                    print(f"Invalid evaluation: {error}")
                    continue
                evaluations.append(evaluation)
                break

        total_weight = sum(e.weight_percentage for e in evaluations)
        if total_weight != TOTAL_WEIGHT_PERCENTAGE:
            print(
                f"\nThe sum of weight percentages must be "
                f"{TOTAL_WEIGHT_PERCENTAGE}, but is {total_weight}."
            )
            print("Please re-enter all evaluations.\n")
            continue

        return evaluations


def main() -> None:
    print("=== CS-GradeCalculator ===")

    student_code = _read_non_empty_string("Student code: ")
    student_identifier = _read_non_empty_string("Student identifier: ")

    evaluations = _read_evaluations()

    attendance_percentage = _read_float(
        "\nStudent attendance percentage (0–100 with threshold being 70): "
    )
    attendance_ratio = attendance_percentage / 100.0

    extra_points_enabled = _read_yes_no(
        "Are extra points enabled for this year?"
    )

    try:
        calculator = GradeCalculator(evaluations)
        final_grade = calculator.calculate_final_grade(
            attendance_ratio=attendance_ratio,
            extra_points_enabled=extra_points_enabled,
        )
    except ValueError as error:
        print(f"\nError while calculating final grade: {error}")
        return

    print("\n=== Result ===")
    print(f"Student code: {student_code}")
    print(f"Student identifier: {student_identifier}")
    print(f"Final grade: {final_grade:.2f}")


if __name__ == "__main__":
    main()
