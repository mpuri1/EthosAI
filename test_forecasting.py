import unittest
from analytics import ComplianceForecaster

class TestComplianceForecasting(unittest.TestCase):
    def setUp(self):
        self.forecaster = ComplianceForecaster()

    def test_improving_trend(self):
        # Risk scores going down
        history = [10.0, 8.0, 6.0, 4.0]
        result = self.forecaster.predict_maturity_drift(history)
        self.assertEqual(result["trend"], "IMPROVING")
        self.assertLess(result["forecast_next_score"], history[-1])

    def test_degrading_trend(self):
        # Risk scores going up rapidly
        history = [10.0, 12.0, 14.0, 16.0]
        result = self.forecaster.predict_maturity_drift(history)
        self.assertEqual(result["trend"], "DEGRADING")
        self.assertGreater(result["forecast_next_score"], history[-1])
        self.assertTrue(result["is_risk_alert"])

    def test_stable_trend(self):
        # All scores identical — slope is zero
        history = [8.0, 8.0, 8.0, 8.0]
        result = self.forecaster.predict_maturity_drift(history)
        self.assertEqual(result["trend"], "STABLE")
        self.assertAlmostEqual(result["drift_rate_per_audit"], 0.0)

    def test_minimum_valid_input(self):
        # Exactly two points — the minimum required for a valid forecast
        history = [5.0, 7.0]
        result = self.forecaster.predict_maturity_drift(history)
        self.assertEqual(result["trend"], "DEGRADING")
        self.assertIsNotNone(result["forecast_next_score"])

    def test_insufficient_data_returns_consistent_keys(self):
        # Single point should return the same key shape as a normal result
        history = [10.0]
        result = self.forecaster.predict_maturity_drift(history)
        for key in ("current_score", "forecast_next_score", "drift_rate_per_audit", "trend", "is_risk_alert"):
            self.assertIn(key, result, f"Missing key '{key}' in insufficient-data result")
        self.assertIsNone(result["forecast_next_score"])
        self.assertFalse(result["is_risk_alert"])

    def test_empty_history_returns_consistent_keys(self):
        # Empty list should not crash and should return the same key shape
        result = self.forecaster.predict_maturity_drift([])
        for key in ("current_score", "forecast_next_score", "drift_rate_per_audit", "trend", "is_risk_alert"):
            self.assertIn(key, result, f"Missing key '{key}' in empty-history result")
        self.assertIsNone(result["forecast_next_score"])

if __name__ == "__main__":
    unittest.main()
