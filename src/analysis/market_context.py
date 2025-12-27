from src.core.base_analyzer import BaseAnalyzer

class MarketContextAnalyzer(BaseAnalyzer):
    def run(self):
        return {
            "competitors": ["MSFT", "GOOGL", "AMZN"],
            "index_inclusions": ["S&P 500", "NASDAQ 100"],
            "market_maturity": "High"
        }
