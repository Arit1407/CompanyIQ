"""
Fetch Latest Company News using Google News RSS

Author: CompanyIQ
"""

import feedparser
import pandas as pd
from bs4 import BeautifulSoup

from config.config import (
    COMPANY_MASTER_PATH,
    NEWS_DATASET_PATH
)

# =====================================================
# SETTINGS
# =====================================================

MAX_ARTICLES = 5

# =====================================================
# READ COMPANY MASTER
# =====================================================

companies = pd.read_csv(COMPANY_MASTER_PATH)

all_news = []

# =====================================================
# FETCH NEWS
# =====================================================

for _, company in companies.iterrows():

    company_id = company["company_id"]
    ticker = company["ticker"]
    company_name = company["company_name"]

    print(f"Fetching news for {company_name}...")

    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={company_name.replace(' ', '+')}+business"
        f"&hl=en-US&gl=US&ceid=US:en"
    )

    feed = feedparser.parse(rss_url)

    if len(feed.entries) == 0:
        print("   No news found.")
        continue

    for article in feed.entries[:MAX_ARTICLES]:

        summary = article.get("summary", "")
        summary = BeautifulSoup(summary, "html.parser").get_text()

        all_news.append({

            "company_id": company_id,

            "ticker": ticker,

            "company_name": company_name,

            "title": article.get("title", ""),

            "published": article.get("published", ""),

            "summary": summary,

            "link": article.get("link", "")

        })

# =====================================================
# CREATE DATAFRAME
# =====================================================

news_df = pd.DataFrame(all_news)

# Remove duplicate news
news_df.drop_duplicates(
    subset=["company_name", "title"],
    inplace=True
)

# =====================================================
# SAVE
# =====================================================

news_df.to_csv(
    NEWS_DATASET_PATH,
    index=False,
    encoding="utf-8"
)

# =====================================================
# SUMMARY
# =====================================================

print("\n=========================================")
print(" News Collection Completed")
print("=========================================")
print(f"Companies Processed : {len(companies)}")
print(f"Articles Collected  : {len(news_df)}")
print(f"Saved To            : {NEWS_DATASET_PATH}")
print("=========================================")