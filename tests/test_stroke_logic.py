import unittest

from stroke_logic import build_feature_row, compute_risk_summary


class BuildFeatureRowTests(unittest.TestCase):
    def test_build_feature_row_matches_feature_order_and_values(self):
        feature_names = [
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "bmi",
            "gender_Female",
            "gender_Male",
            "work_type_Private",
            "work_type_Self-employed",
            "smoking_status_never smoked",
            "smoking_status_smokes",
        ]

        row = build_feature_row(
            age=63,
            gender="Female",
            work_type="Private",
            smoking_status="never smoked",
            hypertension=True,
            heart_disease=False,
            avg_glucose_level=155.5,
            bmi=23.4,
            feature_names=feature_names,
        )

        self.assertEqual(feature_names, list(row.columns))
        self.assertEqual(63.0, row.iloc[0]["age"])
        self.assertEqual(1, row.iloc[0]["hypertension"])
        self.assertEqual(0, row.iloc[0]["heart_disease"])
        self.assertEqual(1, row.iloc[0]["gender_Female"])
        self.assertEqual(0, row.iloc[0]["gender_Male"])
        self.assertEqual(1, row.iloc[0]["work_type_Private"])
        self.assertEqual(0, row.iloc[0]["work_type_Self-employed"])
        self.assertEqual(1, row.iloc[0]["smoking_status_never smoked"])
        self.assertEqual(0, row.iloc[0]["smoking_status_smokes"])

    def test_build_feature_row_defaults_missing_categories_to_zero(self):
        feature_names = [
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "bmi",
            "gender_Other",
            "work_type_Never_worked",
            "smoking_status_Unknown",
        ]

        row = build_feature_row(
            age=45,
            gender="Male",
            work_type="Private",
            smoking_status="smokes",
            hypertension=False,
            heart_disease=False,
            avg_glucose_level=100,
            bmi=21.0,
            feature_names=feature_names,
        )

        self.assertEqual(0, row.iloc[0]["gender_Other"])
        self.assertEqual(0, row.iloc[0]["work_type_Never_worked"])
        self.assertEqual(0, row.iloc[0]["smoking_status_Unknown"])


class ComputeRiskSummaryTests(unittest.TestCase):
    def test_severe_fast_symptom_forces_emergency_score(self):
        summary = compute_risk_summary(
            ml_probability=0.05,
            fast_values={"face": 0, "arm": 15, "speech": 0, "headache": 0},
        )

        self.assertEqual(99, summary["final_score"])
        self.assertIn("GỌI CẤP CỨU 115", summary["override_msg"])

    def test_two_clear_fast_symptoms_raise_floor_to_80(self):
        summary = compute_risk_summary(
            ml_probability=0.10,
            fast_values={"face": 10, "arm": 10, "speech": 0, "headache": 0},
        )

        self.assertEqual(80, summary["final_score"])
        self.assertIn("tối thiểu 80/100", summary["override_msg"])

    def test_exact_two_ro_fast_symptoms_trigger_floor_without_severe_override(self):
        summary = compute_risk_summary(
            ml_probability=0.01,
            fast_values={"face": 10, "arm": 0, "speech": 10, "headache": 0},
        )

        self.assertEqual(80, summary["final_score"])
        self.assertNotIn("GỌI CẤP CỨU 115", summary["override_msg"])
        self.assertIn("mức RÕ hoặc cao hơn", summary["override_msg"])

    def test_regular_case_uses_combined_score_without_override(self):
        summary = compute_risk_summary(
            ml_probability=0.50,
            fast_values={"face": 5, "arm": 0, "speech": 0, "headache": 0},
        )

        self.assertEqual(25, summary["final_score"])
        self.assertIsNone(summary["override_msg"])


if __name__ == "__main__":
    unittest.main()
