from src.analysis.cost_scale import CostScaleAnalyzer
from src.analysis.supply_chain import SupplyChainAnalyzer
from src.analysis.market_context import MarketContextAnalyzer
from src.analysis.stakeholders import StakeholdersAnalyzer
from src.analysis.internal_structure import InternalStructureAnalyzer
from src.analysis.security import SecurityAnalyzer
from src.analysis.market_position import MarketPositionAnalyzer

ANALYZERS = [
    CostScaleAnalyzer,
    SupplyChainAnalyzer,
    MarketContextAnalyzer,
    StakeholdersAnalyzer,
    InternalStructureAnalyzer,
    SecurityAnalyzer,
    MarketPositionAnalyzer
]

def run_full_analysis(company):
    report = {}

    for analyzer_cls in ANALYZERS:
        analyzer = analyzer_cls(company)
        report[analyzer_cls.__name__] = analyzer.run()

    return report
