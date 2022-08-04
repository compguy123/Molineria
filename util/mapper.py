from typing import Any, Type, TypeVar

T = TypeVar("T")


class TupleMapper:
    @staticmethod
    def map(type: Type[T], tuple: tuple) -> T:
        return type(*tuple)

    @staticmethod
    def map_all(type: Type[T], tuples: list[tuple]) -> list[T]:
        return [TupleMapper.map(type, x) for x in tuples]

    @staticmethod
    def map_multi(types: list[Type[T]], tuple: tuple) -> dict[Type[T], Any]:
        result: dict[Type[T], T] = {}
        next_stopping_point = 0
        step_len = 1
        starting_point = 0

        for t in types:
            next_stopping_point = next_stopping_point + len(vars(t()))
            tup = tuple[starting_point:next_stopping_point:step_len]
            starting_point = next_stopping_point

            rec = TupleMapper.map(t, tup)
            result[t] = rec

        return result

    @staticmethod
    def map_multi_all(
        types: list[Type[T]], tuples: list[tuple]
    ) -> list[dict[Type[T], Any]]:
        return [TupleMapper.map_multi(types, tup) for tup in tuples]
