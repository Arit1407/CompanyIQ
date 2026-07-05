"""
Hybrid Valuation Dataset Builder
Alpha Vantage + yfinance fallback
"""

import json
import pandas as pd
import yfinance as yf

from config.config import (
    COMPANY_MASTER_PATH,
    OVERVIEW_PATH,
    VALUATION_DATASET_PATH
)

# ===================================================
# Check valid Alpha Overview
# ===================================================

def is_valid_overview(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return (
            "MarketCapitalization" in data and
            data.get("MarketCapitalization") not in [None, "", "None"]
        )

    except Exception:
        return False


# ===================================================
# Yahoo Finance Fallback
# ===================================================

def fetch_yfinance(yahoo_ticker):

    try:

        stock = yf.Ticker(yahoo_ticker)

        info = stock.info

        return {

            "market_cap": info.get("marketCap"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),
            "country": info.get("country"),

            "sector": info.get("sector"),
            "industry": info.get("industry"),

            "pe_ratio": info.get("trailingPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),

            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue"),

            "dividend_yield": info.get("dividendYield"),

            "beta": info.get("beta"),

            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),

            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins")

        }

    except Exception as e:

        print(f"yfinance failed for {yahoo_ticker}: {e}")
        return None


# ===================================================
# Load Company Master
# ===================================================

companies = pd.read_csv(COMPANY_MASTER_PATH)

valuation_records = []

print(f"\nProcessing {len(companies)} companies...\n")


# ===================================================
# Main Loop
# ===================================================

for _, company in companies.iterrows():

    company_id = company["company_id"]
    ticker = company["ticker"]
    yahoo_ticker = company["yahoo_ticker"]
    company_name = company["company_name"]

    print(f"Processing {company_name}")

    overview_file = OVERVIEW_PATH / f"{ticker}.json"

    data = None
    source = None

    # ===================================================
    # Alpha Vantage
    # ===================================================

    try:

        if is_valid_overview(overview_file):

            with open(
                overview_file,
                "r",
                encoding="utf-8"
            ) as file:

                overview = json.load(file)

            data = {

                "market_cap": overview.get("MarketCapitalization"),
                "currency": overview.get("Currency"),
                "exchange": overview.get("Exchange"),
                "country": overview.get("Country"),

                "sector": overview.get("Sector"),
                "industry": overview.get("Industry"),

                "pe_ratio": overview.get("PERatio"),
                "peg_ratio": overview.get("PEGRatio"),
                "price_to_book": overview.get("PriceToBookRatio"),

                "eps": overview.get("EPS"),
                "book_value": overview.get("BookValue"),

                "dividend_yield": overview.get("DividendYield"),

                "beta": overview.get("Beta"),

                "roe": overview.get("ReturnOnEquityTTM"),
                "roa": overview.get("ReturnOnAssetsTTM"),

                "profit_margin": overview.get("ProfitMargin"),
                "operating_margin": overview.get("OperatingMarginTTM")

            }

            source = "alpha_vantage"

        else:
            raise Exception("Invalid Alpha Overview")

    except Exception:

        # ===================================================
        # Yahoo Finance Fallback
        # ===================================================

        print(f"Using yfinance for {ticker} ({yahoo_ticker})")

        data = fetch_yfinance(yahoo_ticker)
        source = "yfinance"

    # ===================================================
    # Skip if both fail
    # ===================================================

    if data is None:
        print(f"Skipping {ticker}")
        continue

    # ===================================================
    # Append
    # ===================================================

    data.update({

        "company_id": company_id,
        "ticker": ticker,
        "company_name": company_name,
        "source": source

    })

    valuation_records.append(data)


# ===================================================
# Save Dataset
# ===================================================

df = pd.DataFrame(valuation_records)

df.to_csv(
    VALUATION_DATASET_PATH,
    index=False
)

print("\n===================================")
print("Hybrid Valuation Dataset Created")
print("===================================")
print(f"Total Companies : {len(df)}")
print(f"Saved To : {VALUATION_DATASET_PATH}")