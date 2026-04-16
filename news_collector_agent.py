import feedparser
from pymongo import MongoClient
from datetime import datetime, UTC
# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["market_intelligence"]

collection = db["live_news"]

# Google News RSS
RSS_URL = "https://news.google.com/rss/search?q=AI+tools"

def collect_news():

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:

        news_doc = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "collected_at": datetime.now(UTC),
            "source": "google_news_rss"
        }

        collection.insert_one(news_doc)

    print("Live news collected successfully.")

collect_news()
