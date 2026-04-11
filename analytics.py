from typing import Dict, Any, List
import time
import numpy as np
from sklearn.linear_model import LinearRegression

class ComplianceAnalytics:
    """
    Lead-Level Analytics for AI Compliance and Risk.
    Tracks Token ROI and Quantitative Risk Severity.
    """
    
    # Industry Baselines (Senior Legal Policy Auditor)
    MANUAL_RESEARCH_BASE_HOURS = 6.0
    GPT_5_4_NANO_COST_PER_MILLION = 0.05
    
    def __init__(self, legal_research_hourly_rate: float = 250.0):
        self.legal_rate = legal_research_hourly_rate

    def calculate_research_roi(self, execution_time_sec: float, total_tokens: int) -> Dict[str, Any]:
        """
        Calculates the economic value of the multi-agent research.
        Compares agentic speed/cost against a Senior Legal Policy Auditor.
        """
        manual_cost = self.MANUAL_RESEARCH_BASE_HOURS * self.legal_rate
        llm_cost = (total_tokens / 1_000_000) * self.GPT_5_4_NANO_COST_PER_MILLION
        
        # Calculate Speed Advantage
        human_seconds = self.MANUAL_RESEARCH_BASE_HOURS * 3600
        speedup_x = human_seconds / max(execution_time_sec, 0.1)
        
        return {
            "manual_legal_cost": round(manual_cost, 2),
            "agent_token_cost": round(llm_cost, 6),
            "net_savings": round(manual_cost - llm_cost, 2),
            "efficiency_multiplier": round(manual_cost / max(llm_cost, 0.000001), 1),
            "execution_time_sec": round(execution_time_sec, 2),
            "speedup_factor": round(speedup_x, 1)
        }

    def generate_risk_matrix(self, risk_count: int, critical_count: int) -> Dict[str, Any]:
        """
        Provides a prioritized risk severity matrix.
        """
        score = (risk_count * 2) + (critical_count * 5)
        severity = "LOW"
        if score > 15: severity = "CRITICAL"
        elif score > 8: severity = "HIGH"
        elif score > 4: severity = "MEDIUM"
        
        return {
            "risk_score": score,
            "severity_tier": severity,
            "status": "🛑 BLOCKED" if severity == "CRITICAL" else "⚠️ CAUTION" if severity == "HIGH" else "✅ PASSED"
        }

class ComplianceForecaster:
    """
    Predictive Governance Engine.
    Uses linear regression to forecast future compliance drift and maturity.
    """
    
    def __init__(self):
        self.model = LinearRegression()

    def predict_maturity_drift(self, historical_scores: List[float]) -> Dict[str, Any]:
        """
        Forecasts the next compliance score based on historical trend.
        Returns the forecast, trend direction, and drift rate.
        """
        if len(historical_scores) < 2:
            return {"forecast": None, "drift_rate": 0, "status": "Insufficient Data"}

        # Prepare data for regression (X = time index, y = score)
        X = np.array(range(len(historical_scores))).reshape(-1, 1)
        y = np.array(historical_scores)
        
        self.model.fit(X, y)
        
        # Predict the next point (N+1)
        next_index = np.array([[len(historical_scores)]])
        forecast = self.model.predict(next_index)[0]
        
        # Calculate drift (slope)
        drift = self.model.coef_[0]
        
        status = "IMPROVING" if drift < 0 else "STABLE" if drift == 0 else "DEGRADING"
        
        return {
            "current_score": historical_scores[-1],
            "forecast_next_score": round(float(forecast), 2),
            "drift_rate_per_audit": round(float(drift), 2),
            "trend": status,
            "is_risk_alert": forecast > 15  # Alert if forecasted to cross CRITICAL threshold
        }

    def simulate_historical_data(self, points: int = 5) -> List[float]:
        """
        Generates realistic simulation data for dashboard testing.
        Shows a slight upward drift (increasing risk) over time.
        """
        base = [4, 5, 8, 6, 9] # Sample risk scores
        return base[:points]
