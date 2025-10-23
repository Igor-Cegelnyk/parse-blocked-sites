from functools import wraps
from typing import TYPE_CHECKING, Callable
import time


if TYPE_CHECKING:
    import logging


def profile(log: "logging.Logger") -> Callable:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def inner(*args, **kwargs):
            time_start = time.perf_counter()

            try:
                result = await func(*args, **kwargs)
                time_end = time.perf_counter()

                log.info(
                    f"=== Функція {func.__name__} Час виконання: {round(time_end - time_start, 2)} секунд === \n"
                )

                return result
            except Exception as error:
                log.error(
                    f"!!!!! ПОМИЛКА у функції {func.__name__}: "
                    f"Тип помилки: {type(error).__name__}, "
                    f"Помилка: {error} !!!!! \n"
                )
                raise error

        return inner

    return wrapper
