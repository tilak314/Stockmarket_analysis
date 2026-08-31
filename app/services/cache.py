import json
import redis
from datetime import datetime, timezone


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def get_cached_analysis(ticker):
    data = redis_client.get(f"stock:{ticker}")

    if data:
        return json.loads(data)

    return None


def set_cached_analysis(ticker, analysis, ttl=3600):

    analysis["cached_at"] = datetime.now(timezone.utc).isoformat()

    redis_client.setex(
        f"stock:{ticker}",
        ttl,
        json.dumps(analysis)
    )