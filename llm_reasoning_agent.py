import os

from datetime import UTC, datetime

from groq import APIError, Groq
from pymongo import MongoClient

GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MongoDB
client_db = MongoClient("mongodb://localhost:27017/")
db = client_db["market_intelligence"]

news_collection = db["live_news"]
insight_collection = db["market_insights"]


def generate_insight():    
    if not GROQ_API_KEY:
        print("Missing GROQ_API_KEY environment variable.")
        return

    client_ai = Groq(api_key=GROQ_API_KEY)

    # Get latest 5 news
    latest_news = list(news_collection.find().sort("collected_at", -1).limit(5))

    if not latest_news:
        print("No news found in 'live_news'. Add news first, then run this script again.")
        return

    news_text = ""
    for news in latest_news:
        title = news.get("title", "").strip()
        if title:
            news_text += f"- {title}\n"

    if not news_text.strip():
        print("News records were found, but none contained a usable 'title'.")
        return

    prompt = f"""
You are a market intelligence analyst.

Analyze these latest news headlines:

{news_text}

Return:

1. Key Market Trends
2. Competitor Activities
3. Possible Opportunities
"""

    try:
        response = client_ai.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except APIError as exc:
        print(f"Groq API error: {exc}")
        return
    except Exception as exc:
        print(f"Unexpected error while generating insight: {exc}")
        return

    insight_text = response.choices[0].message.content

    insight_doc = {
        "insight": insight_text,
        "generated_at": datetime.now(UTC),
        "source": "groq_llm_agent",
        "model": GROQ_MODEL,
    }

    insight_collection.insert_one(insight_doc)
    print("Market insight generated.")


if __name__ == "__main__":
    generate_insight()
