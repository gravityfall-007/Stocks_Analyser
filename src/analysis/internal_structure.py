from src.core.base_analyzer import BaseAnalyzer

class InternalStructureAnalyzer(BaseAnalyzer):
    def run(self):
        return {
            "board_structure": "Independent board",
            "employee_count": self.company.fundamentals.get("fullTimeEmployees", "N/A"),
            "org_complexity": "High"
        }
