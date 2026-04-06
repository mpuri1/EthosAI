import json
from typing import Dict, Any

class ComplianceAnalytics:
    """
    Lead-Level Analytics for AI Compliance and Risk.
    Tracks Token ROI and Quantitative Risk Severity.
    """
    
    def __init__(self, legal_research_hourly_rate: float = 250.0):
        self.legal_rate = legal_research_hourly_rate
        # GPT-5.4 Nano estimate: $0.05 / 1M tokens
        self.cost_per_million = 0.05

    def calculate_research_roi(self, execution_time_sec: float, total_tokens: int) -> Dict[str, float]:
        """
        Calculates the economic value of the multi-agent research.
        Compares agentic speed/cost against a Senior Legal Policy Auditor.
        """
        # Assumptions: Human takes 6 hours for a thorough regulatory scan
        manual_research_hours = 6.0
        manual_cost = manual_research_hours * self.legal_rate
        
        llm_cost = (total_tokens / 1_000_000) * self.cost_per_million
        
        return {
            "manual_legal_cost": round(manual_cost, 2),
            "agent_token_cost": round(llm_cost, 6),
            "net_savings": round(manual_cost - llm_cost, 2),
            "efficiency_multiplier": round(manual_cost / max(llm_cost, 0.000001), 1)
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
