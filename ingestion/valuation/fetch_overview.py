"""
Fetch Company Overview Data from Alpha Vantage

Author: CompanyIQ Team
"""

import json
import time
import requests
import pandas as pd

from config.config import (
    COMPANY_MASTER_PATH,
    OVERVIEW_PATH,
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_BASE_URL
)

companies = pd.read_csv(COMPANY_MASTER_PATH)

print(f"\nTotal Companies : {len(companies)}")

for index, company in companies.iterrows():

    company_name = company["company_name"]
    ticker = company["ticker"]

    print(f"\n[{index + 1}/{len(companies)}] Fetching Overview for {company_name} ({ticker})")

    output_file = OVERVIEW_PATH / f"{ticker}.json"

    if output_file.exists():
        print("Already exists. Skipping...")
        continue

    params = {
        "function": "OVERVIEW",
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

print("\nOverview Collection Completed!")