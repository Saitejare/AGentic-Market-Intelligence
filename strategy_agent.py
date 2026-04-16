"""Strategy agent module."""

import os
from pymongo import MongoClient
from datetime import datetime, UTC
from groq import Groq

# Groq API
client_ai = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# MongoDB
client_db = MongoClient("mongodb://localhost:27017/")
db = client_db["market_intelligence"]

insight_collection = db["market_insights"]
strategy_collection = db["market_strategies"]


def generate_strategy():

    # Get latest insight
    latest_insight = insight_collection.find().sort(
        "generated_at", -1
    ).limit(1)

    insight_text = ""

    for ins in latest_insight:
        insight_text = ins["insight"]

    prompt = f"""
You are a business strategy expert.

Based on this market insight:

{insight_text}

Generate:

1 Business Strategy Recommendation
2 Risk Level (Low/Medium/High)
3 Expected Impact
"""

    response = client_ai.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    strategy_text = response.choices[0].message.content

    strategy_doc = {
        "strategy": strategy_text,
        "generated_at": datetime.now(UTC),
        "source": "strategy_agent"
    }

    strategy_collection.insert_one(strategy_doc)

    print("Strategy generated successfully.")


# Run once test
generate_strategy()
