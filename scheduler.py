from apscheduler.schedulers.blocking import BlockingScheduler

# Import agents
from news_collector_agent import collect_news
from trend_collector_agent import collect_trends
from llm_reasoning_agent import generate_insight
from strategy_agent import generate_strategy


# -------------------------
# Safe wrapper (important)
# Prevents scheduler crash
# -------------------------

def safe_run(job_func, job_name):
    try:
        print(f"Running job: {job_name}")
        job_func()
        print(f"Completed job: {job_name}")

    except Exception as e:
        print(f"Error in {job_name}: {e}")


# -------------------------
# Create Scheduler
# -------------------------

scheduler = BlockingScheduler()


# -------------------------
# Job 1 — News Collector
# -------------------------

scheduler.add_job(
    lambda: safe_run(collect_news, "News Collector"),
    trigger='interval',
    minutes=10,
    id='news_job',
    replace_existing=True
)


# -------------------------
# Job 2 — Trend Collector
# -------------------------

scheduler.add_job(
    lambda: safe_run(collect_trends, "Trend Collector"),
    trigger='interval',
    minutes=60,
    id='trend_job',
    replace_existing=True
)


# -------------------------
# Job 3 — LLM Insight Agent
# -------------------------

scheduler.add_job(
    lambda: safe_run(generate_insight, "Insight Generator"),
    trigger='interval',
    minutes=20,
    id='insight_job',
    replace_existing=True
)


# -------------------------
# Job 4 — Strategy Agent
# -------------------------

scheduler.add_job(
    lambda: safe_run(generate_strategy, "Strategy Generator"),
    trigger='interval',
    minutes=25,
    id='strategy_job',
    replace_existing=True
)

from alert_agent import generate_alert

scheduler.add_job(
    lambda: safe_run(generate_alert, "Alert Generator"),
    trigger='interval',
    minutes=15,
    id='alert_job',
    replace_existing=True
)
# -------------------------
# Start Scheduler
# -------------------------

print("🚀 Scheduler running...")
print("Jobs:")
print(" - News every 10 minutes")
print(" - Trends every 60 minutes")
print(" - Insights every 20 minutes")
print(" - Strategies every 25 minutes")

scheduler.start()
