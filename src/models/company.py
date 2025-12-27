class Company:
    """
    Central company object passed through the pipeline.
    """

    def __init__(self, ticker, name, sector):
        self.ticker = ticker
        self.name = name
        self.sector = sector

        self.market_data = None
        self.fundamentals = None
