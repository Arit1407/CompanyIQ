"""
Hybrid Financial Dataset Builder
Alpha Vantage + yfinance fallback (fixed with yahoo_ticker support)
"""

import json
import pandas as pd
import yfinance as yf

from config.config import (
    COMPANY_MASTER_PATH,
    INCOME_STATEMENT_PATH,
    BALANCE_SHEET_PATH,
    CASH_FLOW_PATH,
    FINANCIAL_DATASET_PATH
)

# ===================================================
# Helper: Validate Alpha JSON
# ===================================================

def is_valid_alpha(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return (
            "annualReports" in data and
            len(data["annualReports"]) > 0
        )

    except Exception:
        return False


# ===================================================
# Helper: Safe yfinance extractor
# ===================================================

def safe(df, key):

    try:
        if df is None or df.empty:
            return None

        if key not in df.index:
            return None

        value = df.loc[key].iloc[0]

        if pd.isna(value):
            return None

        return value

    except Exception:
        return None


# ===================================================
# yfinance fallback
# ===================================================

def fetch_yfinance(yahoo_ticker):

    try:
        stock = yf.Ticker(yahoo_ticker)

        fin = stock.financials
        bal = stock.balance_sheet
        cash = stock.cashflow

        return {
            "revenue": safe(fin, "Total Revenue"),
            "gross_profit": safe(fin, "Gross Profit"),
            "operating_income": safe(fin, "Operating Income"),
            "net_income": safe(fin, "Net Income"),

            "total_assets": safe(bal, "Total Assets"),
            "total_liabilities": safe(bal, "Total Liabilities Net Minority Interest"),
            "shareholder_equity": safe(bal, "Stockholders Equity"),
            "cash": safe(bal, "Cash And Cash Equivalents"),

            "operating_cash_flow": safe(cash, "Operating Cash Flow"),
            "capital_expenditure": safe(cash, "Capital Expenditure")
        }

    except Exception as e:
        print(f"yfinance failed for {yahoo_ticker}: {e}")
        return None


# ===================================================
# Load companies
# ===================================================

companies = pd.read_csv(COMPANY_MASTER_PATH)

records = []

print(f"\nProcessing {len(companies)} companies...\n")


# ===================================================
# MAIN LOOP
# ===================================================

for _, company in companies.iterrows():

    company_id = company["company_id"]
    ticker = company["ticker"]
    company_name = company["company_name"]
    yahoo_ticker = company["yahoo_ticker"]

    print(f"Processing {company_name} ({ticker})")

    data = None
    source = None

    # ===================================================
    # Alpha Vantage Path
    # ===================================================

    income_file = INCOME_STATEMENT_PATH / f"{ticker}.json"
    balance_file = BALANCE_SHEET_PATH / f"{ticker}.json"
    cash_file = CASH_FLOW_PATH / f"{ticker}.json"

    try:

        if (
            is_valid_alpha(income_file)
            and is_valid_alpha(balance_file)
            and is_valid_alpha(cash_file)
        ):

            with open(income_file, "r") as f:
                income_json = json.load(f)

            with open(balance_file, "r") as f:
                balance_json = json.load(f)

            with open(cash_file, "r") as f:
                cash_json = json.load(f)

            income = income_json["annualReports"][0]
            balance = balance_json["annualReports"][0]
            cashflow = cash_json["annualReports"][0]

            data = {
                "revenue": income.get("totalRevenue"),
                "gross_profit": income.get("grossProfit"),
                "operating_income": income.get("operatingIncome"),
                "net_income": income.get("netIncome"),

                "total_assets": balance.get("totalAssets"),
                "total_liabilities": balance.get("totalLiabilities"),
                "shareholder_equity": balance.get("totalShareholderEquity"),
                "cash": balance.get("cashAndCashEquivalentsAtCarryingValue"),

                "operating_cash_flow": cashflow.get("operatingCashflow"),
                "capital_expenditure": cashflow.get("capitalExpenditures")
            }

            source = "alpha_vantage"

        else:
            raise Exception("Invalid Alpha data")

    except Exception:

        # ===================================================
        # Fallback → yfinance
        # ===================================================

        print(f"Using yfinance for {ticker} ({yahoo_ticker})")

        data = fetch_yfinance(yahoo_ticker)
        source = "yfinance"

    # ===================================================
    # Skip if both fail
    # ===================================================

    if data is None:
        print(f"Skipping {ticker} completely")
        continue

    # ===================================================
    # Append record
    # ===================================================

    data.update({
        "company_id": company_id,
        "ticker": ticker,
        "company_name": company_name,
        "source": source
    })

    records.append(data)


# ===================================================
# Save dataset
# ===================================================

df = pd.DataFrame(records)

df.to_csv(FINANCIAL_DATASET_PATH, index=False)

print("\n===================================")
print("Financial Dataset Created (HYBRID FIXED)")
print("===================================")
print(f"Total Companies Processed : {len(df)}")
print(f"Saved To : {FINANCIAL_DATASET_PATH}")