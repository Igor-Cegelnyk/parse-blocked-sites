from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from celery.schedules import crontab

from backend.config import settings, Logger

log = Logger().get_logger()

celery_app = Celery(
    "app.celery.celery_app",
    broker=settings.redis.celery_url_backend,
    backend=settings.redis.celery_url_backend,
)


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    logger.handlers = []
    logger.addHandler(log.handlers[0])
    logger.setLevel(log.level)


@after_setup_task_logger.connect
def setup_celery_task_logger(logger, *args, **kwargs):
    logger.handlers = []
    logger.addHandler(log.handlers[0])
    logger.setLevel(log.level)


celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Kiev",
    enable_utc=False,
    task_default_queue="parse_queue",
    result_expires=settings.redis.expires,
    worker_send_task_events=True,
)


celery_app.conf.beat_schedule = {
    "run_parse_domain_task": {
        "task": "backend.celery.tasks.parse_domain_task.run_parse_domain_task",
        "schedule": crontab(minute="*/5"),
    },
}

celery_app.autodiscover_tasks(["backend.celery.tasks"])
