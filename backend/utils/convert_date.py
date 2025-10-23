from datetime import date, datetime, time
import pytz

TZ = pytz.timezone("Europe/Kiev")


def to_tz_datetime(ts: int) -> datetime:
    """Converted UNIX timestamp in datetime for timezone Europe/Kiev"""
    return datetime.fromtimestamp(ts, tz=TZ)


def current_date_int() -> int:
    """Python default: YYYYMMDD"""
    return int(datetime.now(TZ).strftime("%Y%m%d"))


def current_time_int() -> int:
    """Python default: HHMMSS"""
    return int(datetime.now(TZ).strftime("%H%M%S"))


def date_str_to_int(date_str: str | None = None) -> int:
    """

    :param date_str: "2025-10-01"
    :return: 20251001
    """
    if date_str:
        return int(datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d"))
    return int(date.today().strftime("%Y%m%d"))


def date_int_to_str(date_int: int | None = None) -> str | None:
    """

    :param date_int: 20251001
    :return: "2025-10-01"
    """
    if date_int:
        return datetime.strptime(str(date_int), "%Y%m%d").strftime("%Y-%m-%d")
    return None


def time_str_to_int(time_str: str) -> int:
    try:
        h, m, s = map(int, time_str.split(":"))
        t = time(h, m, s)
        return h * 10000 + m * 100 + s
    except ValueError as e:
        raise ValueError(f"Invalid time format: {time_str}") from e


def time_int_to_str(time_int: int) -> str:
    s = str(time_int).rjust(6, "0")
    try:
        h, m, s_ = int(s[0:2]), int(s[2:4]), int(s[4:6])
        return f"{h:02}:{m:02}:{s_:02}"
    except ValueError as e:
        raise ValueError(f"Invalid time integer: {time_int}") from e
