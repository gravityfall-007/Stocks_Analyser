from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """
    Abstract base class for all analysis modules.
    """

    def __init__(self, company):
        self.company = company

    @abstractmethod
    def run(self) -> dict:
        pass
