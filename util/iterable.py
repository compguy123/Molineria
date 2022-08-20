from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")


def flatten(source: Iterable[Iterable[T]]) -> list[T]:
    flat = [item for sub_list in source for item in sub_list]
    return flat


def find(predicate: Callable[[T], bool], source: Iterable[T]) -> T | None:
    if not source or not isinstance(source, list):
        source = []
    for item in source:
        if predicate(item):
            return item
    return None
