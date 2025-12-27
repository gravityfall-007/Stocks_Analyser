def validate_company(company):
    if not company.ticker:
        raise ValueError("Ticker symbol required")
