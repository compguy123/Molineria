def is_null_or_whitespace(value: str | None) -> bool:
    return not value or not value.strip()


def is_null_or_empty(value: str | None) -> bool:
    return not value or value == ""


def from_snake_case_to_pascal_case(value: str) -> str:
    return value.replace("_", " ").title().replace(" ", "")
