import asyncio
from datetime import datetime

from backend.auto_loader.parse_domain.loader_parse_domain import loader_parse_domains
from backend.celery.celery_app import celery_app, log
from backend.config import settings


@celery_app.task(
    bind=True,
    queue="parse_queue",
)
def run_parse_domain_honlapok_task(self):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(loader_parse_domains(settings.website_api))
        else:
            loop.run_until_complete(loader_parse_domains(settings.website_api))
        return {
            "task_id": self.request.id,
            "datetime": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "status": "success",
        }

    except Exception as exc:
        log.info("Помилка: %r", exc)
        self.retry(exc=exc)
        return None


if __name__ == "__main__":
    run_parse_domain_honlapok_task()
