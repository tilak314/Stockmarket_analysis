from celery import Celery

celery = Celery(
    "stockmarket",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.workers.tasks"]
)

celery.autodiscover_tasks([
    "app.workers"
])


# ---celery beat ----------
# uncomment below for automatic triggers

# for specific stock
# celery.conf.beat_schedule = {
#     "analyze-cupid": {
#         "task": "app.workers.tasks.analyze_stock_task",
#         "schedule": 120.0,
#         "args": ("CUPID.NS",),
#     },
# }

# for grp of stocks
# celery.conf.beat_schedule = {
#     "analyze-watchlist-every-12-hours": {
#         "task": "app.workers.tasks.analyze_watchlist",
#         "schedule": 43200.0, # 12 hrs
#     }
# }