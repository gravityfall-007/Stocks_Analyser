import json
import os

def load_available_reports(reports_dir="reports"):
    return [
        f.replace("_report.json", "")
        for f in os.listdir(reports_dir)
        if f.endswith("_report.json")
    ]

def load_report(ticker, reports_dir="reports"):
    path = os.path.join(reports_dir, f"{ticker}_report.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Report not found for {ticker}")
    with open(path, "r") as f:
        return json.load(f)
