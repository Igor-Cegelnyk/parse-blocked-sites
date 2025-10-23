__all__ = ["router"]

from fastapi import APIRouter

from .base import router as base
from .domain import router as domain
from .domain_search import router as domain_search
from .history import router as history
from .file_search import router as file_search


router = APIRouter()

router.include_router(base)
router.include_router(domain)
router.include_router(domain_search)
router.include_router(history)
router.include_router(file_search)
