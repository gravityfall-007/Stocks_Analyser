class AnalyzerRegistry:
    """
    Registry for dynamically managing analyzers.
    """

    _registry = []

    @classmethod
    def register(cls, analyzer):
        cls._registry.append(analyzer)

    @classmethod
    def get_analyzers(cls):
        return cls._registry
