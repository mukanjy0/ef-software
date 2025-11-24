import unittest

from grade_calculator import (
    Evaluation,
    GradeCalculator,
    handle_minimum_attendance,
    handle_extra_points,
    MAX_EVALUATIONS,
)


class TestEvaluation(unittest.TestCase):
    def test_valid_evaluation_is_created(self) -> None:
        evaluation = Evaluation(mark=15.0, weight_percentage=40)
        self.assertEqual(15.0, evaluation.mark)
        self.assertEqual(40, evaluation.weight_percentage)

    def test_invalid_mark_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            Evaluation(mark=25.0, weight_percentage=40)

    def test_invalid_weight_below_range_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            Evaluation(mark=15.0, weight_percentage=0)

    def test_invalid_weight_above_range_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            Evaluation(mark=15.0, weight_percentage=150)


class TestAttendancePolicy(unittest.TestCase):
    def test_attendance_below_threshold_returns_zero(self) -> None:
        result = handle_minimum_attendance(
            grade=15.0,
            attendance_ratio=0.6,
            threshold=0.7,
        )
        self.assertEqual(0.0, result)

    def test_attendance_above_threshold_keeps_grade(self) -> None:
        result = handle_minimum_attendance(
            grade=15.0,
            attendance_ratio=0.8,
            threshold=0.7,
        )
        self.assertEqual(15.0, result)

    def test_invalid_attendance_ratio_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            handle_minimum_attendance(grade=10.0, attendance_ratio=1.2)


class TestExtraPointsPolicy(unittest.TestCase):
    def test_extra_points_disabled_keeps_grade(self) -> None:
        result = handle_extra_points(
            grade=15.0,
            extra_points_enabled=False,
            extra_points=1.0,
        )
        self.assertEqual(15.0, result)

    def test_extra_points_enabled_adds_points(self) -> None:
        result = handle_extra_points(
            grade=15.0,
            extra_points_enabled=True,
            extra_points=1.0,
        )
        self.assertEqual(16.0, result)

    def test_negative_extra_points_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            handle_extra_points(
                grade=15.0,
                extra_points_enabled=True,
                extra_points=-1.0,
            )


class TestGradeCalculator(unittest.TestCase):
    def _build_simple_calculator(self) -> GradeCalculator:
        evaluations = [
            Evaluation(mark=15.0, weight_percentage=40),
            Evaluation(mark=18.0, weight_percentage=60),
        ]
        return GradeCalculator(evaluations)

    def test_calculate_final_grade_normal_case(self) -> None:
        calculator = self._build_simple_calculator()
        grade = calculator.calculate_final_grade(
            attendance_ratio=0.9,
            extra_points_enabled=True,
        )
        # weighted average = (15*40 + 18*60) / 100 = 16.8, plus 1 extra = 17.8
        self.assertAlmostEqual(17.8, grade, places=2)

    def test_calculate_final_grade_without_attendance(self) -> None:
        calculator = self._build_simple_calculator()
        grade = calculator.calculate_final_grade(
            attendance_ratio=0.6,
            extra_points_enabled=True,
        )
        self.assertEqual(0.0, grade)

    def test_calculate_final_grade_without_extra_points(self) -> None:
        calculator = self._build_simple_calculator()
        grade = calculator.calculate_final_grade(
            attendance_ratio=0.9,
            extra_points_enabled=False,
        )
        self.assertAlmostEqual(16.8, grade, places=2)

    def test_zero_evaluations_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            GradeCalculator([])

    def test_more_than_max_evaluations_raises_error(self) -> None:
        evaluations = [
            Evaluation(mark=10.0, weight_percentage=10)
            for _ in range(MAX_EVALUATIONS)
        ]
        extra = Evaluation(mark=10.0, weight_percentage=10)
        evaluations.append(extra)
        with self.assertRaises(ValueError):
            GradeCalculator(evaluations)

    def test_invalid_weight_sum_raises_error(self) -> None:
        evaluations = [
            Evaluation(mark=15.0, weight_percentage=50),
            Evaluation(mark=18.0, weight_percentage=60),
        ]
        with self.assertRaises(ValueError):
            GradeCalculator(evaluations)


if __name__ == "__main__":
    unittest.main()
