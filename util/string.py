from datetime import date, datetime, time


def is_null_or_whitespace(value: str | None) -> bool:
    return not value or not value.strip()


def is_null_or_empty(value: str | None) -> bool:
    return not value or value == ""


def from_snake_case_to_pascal_case(value: str) -> str:
    return value.replace("_", " ").title().replace(" ", "")


def to_snake_case(value: str) -> str:
    return "".join([f"_{c.lower()}" if c.isupper() else c for c in value]).lstrip("_")


def to_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d")


def is_int(value: str) -> bool:
    if value[0] == ("-", "+"):
        return value[1:].isdigit()
    else:
        return value.isdigit()


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_date(value: str) -> bool:
    try:
        to_date(value)
        return True
    except ValueError:
        return False


def is_iso_time(value: str) -> bool:
    try:
        time.fromisoformat(value)
        return True
    except ValueError:
        return False
