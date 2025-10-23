from enum import Enum


class LogStatusEnum(Enum):
    OK = "успішно"
    FAILED = "помилка"
    NO_CHANGES = "змін не виявлено"
