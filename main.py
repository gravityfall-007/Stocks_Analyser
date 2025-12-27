import json
import os
import pandas as pd
from src.models.company import Company
from src.ingestion.market_data import load_market_data
from src.ingestion.fundamentals import load_fundamentals
from src.pipelines.run_company import run_full_analysis
from src.utils.config_loader import load_stocks_config
from src.utils.logger import logger


REPORTS_DIR = "reports"


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    stocks = load_stocks_config()

    logger.info(f"Loaded {len(stocks)} stocks from config")

    for stock in stocks:
        ticker = stock["ticker"]
        name = stock["name"]
        sector = stock["sector"]

        logger.info(f"Running analysis for {ticker}")

        try:
            company = Company(ticker, name, sector)

            company.market_data = load_market_data(ticker)
            # Save market data for visualization
            price_path = f"data/processed/{ticker}_prices.csv"
            company.market_data.to_csv(price_path)

            company.fundamentals = load_fundamentals(ticker)

            report = run_full_analysis(company)

            report_path = os.path.join(
                REPORTS_DIR, f"{ticker}_report.json"
            )

            with open(report_path, "w") as f:
                json.dump(report, f, indent=4)

            logger.info(f"Saved report → {report_path}")

        except Exception as e:
            logger.error(f"Failed analysis for {ticker}: {e}")


if __name__ == "__main__":
    main()
