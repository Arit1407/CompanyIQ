"""
Fetch Income Statement Data from Alpha Vantage

Author: CompanyIQ Team
"""

import json
import time
import requests
import pandas as pd

from config.config import (
    COMPANY_MASTER_PATH,
    INCOME_STATEMENT_PATH,
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_BASE_URL
)

# ==================================================
# Read Company Master
# ==================================================

companies = pd.read_csv(COMPANY_MASTER_PATH)

print(f"\nTotal Companies : {len(companies)}")

# ==================================================
# Fetch Income Statement
# ==================================================

for index, company in companies.iterrows():

    company_id = company["company_id"]
    company_name = company["company_name"]
    ticker = company["ticker"]

    print(f"\n[{index + 1}/{len(companies)}] Fetching Income Statement for {company_name} ({ticker})")

    output_file = INCOME_STATEMENT_PATH / f"{ticker}.json"

    # ----------------------------------------------
    # Skip if already downloaded
    # ----------------------------------------------

    if output_file.exists():
        print("Already exists. Skipping...")
        continue

    # ----------------------------------------------
    # API Parameters
    # ----------------------------------------------

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    # ----------------------------------------------
    # API Request
    # ----------------------------------------------

    try:

        response = requests.get(
            ALPHA_VANTAGE_BASE_URL,
            params=params,
            timeout=30
        )

        data = response.json()

        # API limit reached
        if "Note" in data:
            print("\nAPI Limit Reached!")
            print(data["Note"])
            print("Stopping execution. Run the script again later.")
            break

        # Invalid ticker
        if "Error Message" in data:
            print(f"Error: {ticker} not found.")
            continue

        # Save JSON
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Saved Successfully!")

    except Exception as e:
        print(f"Failed: {e}")

    # ----------------------------------------------
    # Alpha Vantage Rate Limit
    # Free Tier = 5 requests/minute
    # ----------------------------------------------

    time.sleep(15)

print("\nIncome Statement Collection Completed!")