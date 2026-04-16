from pymongo import MongoClient
from datetime import datetime, UTC

client = MongoClient("mongodb://localhost:27017/")
db = client["market_intelligence"]

trend_collection = db["live_trends"]
news_collection = db["live_news"]
alert_collection = db["market_alerts"]


def generate_alert():

    latest_trend = list(
        trend_collection.find()
        .sort("collected_at", -1)
        .limit(1)
    )

    if not latest_trend:
        return

    keywords = latest_trend[0]["top_keywords"]

    alerts = []

    for word, count in keywords:

        if count >= 10:

            # Find related news
            related_news = list(
                news_collection.find(
                    {"title": {"$regex": word}}
                ).limit(3)
            )

            links = []

            for news in related_news:
                links.append(news.get("link", ""))

            alert_data = {
                "keyword": word,
                "count": count,
                "links": links,
                "generated_at": datetime.now(UTC)
            }

            alerts.append(alert_data)

    if alerts:

        alert_collection.insert_one(
            {
                "alerts": alerts,
                "generated_at": datetime.now(UTC)
            }
        )

        print("Detailed alerts generated.")


if __name__ == "__main__":
    generate_alert()
