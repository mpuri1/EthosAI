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

    def test_insufficient_data(self):
        history = [10.0]
        result = self.forecaster.predict_maturity_drift(history)
        self.assertIsNone(result["forecast"])

if __name__ == "__main__":
    unittest.main()
