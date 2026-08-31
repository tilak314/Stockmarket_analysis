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