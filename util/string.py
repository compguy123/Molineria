def is_null_or_whitespace(value: str | None) -> bool:
    return not value or not value.strip()


def is_null_or_empty(value: str | None) -> bool:
    return not value or value == ""


def from_snake_case_to_pascal_case(value: str) -> str:
    return value.replace("_", " ").title().replace(" ", "")


def to_snake_case(value: str) -> str:
    return "".join([f"_{c.lower()}" if c.isupper() else c for c in value]).lstrip("_")