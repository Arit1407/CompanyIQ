"""
Fetch Balance Sheet Data from Alpha Vantage

Author: CompanyIQ Team
"""

import json
import time
import requests
import pandas as pd

from config.config import (
    COMPANY_MASTER_PATH,
    BALANCE_SHEET_PATH,
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_BASE_URL
)

# ==================================================
# Read Company Master
# ==================================================

companies = pd.read_csv(COMPANY_MASTER_PATH)

print(f"\nTotal Companies : {len(companies)}")

# ==================================================
# Fetch Balance Sheet
# ==================================================

for index, company in companies.iterrows():

    company_name = company["company_name"]
    ticker = company["ticker"]

    print(f"\n[{index + 1}/{len(companies)}] Fetching Balance Sheet for {company_name} ({ticker})")

    output_file = BALANCE_SHEET_PATH / f"{ticker}.json"

    if output_file.exists():
        print("Already exists. Skipping...")
        continue

    params = {
        "function": "BALANCE_SHEET",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    try:

        response = requests.get(
            ALPHA_VANTAGE_BASE_URL,
            params=params,
            timeout=30
        )

        data = response.json()

        if "Note" in data:
            print("\nAPI Limit Reached!")
            break

        if "Error Message" in data:
            print(f"Error: {ticker}")
            continue

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Saved Successfully!")

    except Exception as e:
        print(e)

    time.sleep(15)

print("\nBalance Sheet Collection Completed!")