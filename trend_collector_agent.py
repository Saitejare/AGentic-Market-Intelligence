from pymongo import MongoClient
from datetime import datetime, UTC
from collections import Counter
import re

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["market_intelligence"]

news_collection = db["live_news"]
trend_collection = db["live_trends"]


def collect_trends():

    # Get latest news titles
    latest_news = list(
        news_collection.find()
        .sort("collected_at", -1)
        .limit(50)
    )

    if not latest_news:
        print("No news available to extract trends.")
        return

    words = []

    for news in latest_news:

        title = news.get("title", "")

        # Clean text
        clean_words = re.findall(
            r'\b[a-zA-Z]{4,}\b',
            title.lower()
        )

        words.extend(clean_words)

    # Count most common words
    common_words = Counter(words).most_common(10)

    trend_doc = {
    "top_keywords": common_words,
    "trend_date": datetime.now(UTC),
    "collected_at": datetime.now(UTC)
    }

    trend_collection.insert_one(trend_doc)

    print("Trend keywords extracted successfully.")


if __name__ == "__main__":
    collect_trends()
