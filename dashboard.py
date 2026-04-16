"""Dashboard module."""
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_autorefresh import st_autorefresh
st.set_page_config(page_title="Market Intelligence Dashboard")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["market_intelligence"]

news_collection = db["live_news"]
trend_collection = db["live_trends"]
insight_collection = db["market_insights"]
strategy_collection = db["market_strategies"]
alert_collection = db["market_alerts"]


def normalize_alerts(alert_doc):
    """Support both legacy string alerts and newer dict-based alerts."""
    normalized = []
    latest_trend = trend_collection.find_one(sort=[("collected_at", -1)])
    keyword_counts = dict(latest_trend.get("top_keywords", [])) if latest_trend else {}

    for alert in alert_doc.get("alerts", []):
        if isinstance(alert, dict):
            normalized.append(alert)
            continue

        if isinstance(alert, str):
            keyword = alert.split(":", 1)[-1].strip() if ":" in alert else alert.strip()
            related_news = list(
                news_collection.find({"title": {"$regex": keyword, "$options": "i"}}).limit(3)
            )
            normalized.append(
                {
                    "keyword": keyword,
                    "count": keyword_counts.get(keyword),
                    "links": [news.get("link", "") for news in related_news if news.get("link")],
                }
            )

    return normalized

st.set_page_config(page_title="Market Intelligence Dashboard")

st.title("📊 Autonomous Market Intelligence System")
# Auto refresh every 30 seconds
st_autorefresh(
    interval=30 * 1000,
    key="datarefresh"
)

# -------------------------
# Latest News
# -------------------------

st.header("📰 Latest News")

news_data = list(
    news_collection.find()
    .sort("collected_at", -1)
    .limit(10)
)

if news_data:

    news_df = pd.DataFrame(news_data)

    st.dataframe(
        news_df[["title", "published"]]
    )

else:
    st.write("No news available.")

# -------------------------
# Market Insights
# -------------------------

st.header("🧠 Market Insights")

insight_data = list(
    insight_collection.find()
    .sort("generated_at", -1)
    .limit(5)
)

for ins in insight_data:

    st.write(ins["insight"])
    st.write("---")

# -------------------------
# Strategies
# -------------------------

st.header("🎯 Strategy Recommendations")

strategy_data = list(
    strategy_collection.find()
    .sort("generated_at", -1)
    .limit(5)
)

for strat in strategy_data:

    st.write(strat["strategy"])
    st.write("---")
# -------------------------
# Alerts
# -------------------------

st.header("⚠️ Market Alerts")

alerts = list(
    alert_collection.find()
    .sort("generated_at", -1)
    .limit(1)
)

if alerts:

    for alert in normalize_alerts(alerts[0]):

        st.warning(
            f"High Trend: {alert['keyword']}"
        )

        if alert.get("count") is not None:
            st.write(
                f"Mentions: {alert['count']}"
            )

        st.write("Related News:")

        for link in alert.get("links", []):
            st.markdown(f"[Open Article]({link})")

        st.write("---")

# -------------------------
# Trends
# -------------------------

st.header("📈 Market Trends")

trend_data = list(
    trend_collection.find()
    .sort("collected_at", -1)
    .limit(5)
)

if trend_data:

    st.subheader("🔥 Top Trending Keywords")

    latest_trend = trend_data[0]

    if "top_keywords" in latest_trend:

        for word, count in latest_trend["top_keywords"]:
            st.write(f"🔹 {word} — {count}")

    else:
        st.write(f"Trend Date: {latest_trend['trend_date']}")

else:
    st.write("No trend data available.")
st.markdown("""
<style>
.big-title {
    font-size:36px;
    font-weight:bold;
}
.alert-box {
    background-color:#2b2b00;
    padding:10px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)
