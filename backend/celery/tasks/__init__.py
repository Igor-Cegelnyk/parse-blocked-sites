__all__ = (
    "run_parse_domain_honlapok_task",
    "run_parse_domain_reklamoldalak_task",
)

from backend.celery.tasks.parse_domain_honlapok_task import (
    run_parse_domain_honlapok_task,
)
from backend.celery.tasks.parse_domain_reklamoldalak_task import (
    run_parse_domain_reklamoldalak_task,
)
