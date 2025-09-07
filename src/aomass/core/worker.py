"""Celery worker configuration for AOMaaS."""
from celery import Celery

from aomass.config.settings import settings

# Create Celery instance
celery_app = Celery(
    "aomass",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "aomass.core.tasks.indexer",
        "aomass.core.tasks.implementer",
        "aomass.core.tasks.reviewer",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task routes
celery_app.conf.task_routes = {
    "aomass.core.tasks.indexer.*": {"queue": "indexer"},
    "aomass.core.tasks.implementer.*": {"queue": "implementer"},
    "aomass.core.tasks.reviewer.*": {"queue": "reviewer"},
}
