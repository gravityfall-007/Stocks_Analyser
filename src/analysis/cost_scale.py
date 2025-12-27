from src.core.base_analyzer import BaseAnalyzer

class CostScaleAnalyzer(BaseAnalyzer):
    def run(self):
        f = self.company.fundamentals or {}

        revenue = f.get("totalRevenue", 0)
        margin = f.get("operatingMargins", None)

        return {
            "revenue": revenue,
            "operating_margin": margin,
            "economies_of_scale": "High" if revenue and revenue > 1e11 else "Medium"
        }
