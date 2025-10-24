__all__ = ["router"]

from fastapi import APIRouter

from .base import router as base
from .domain import router as domain
from .history import router as history


router = APIRouter()

router.include_router(base)
router.include_router(domain)
router.include_router(history)
