from typing import Any, Type, TypeVar
from util.string import to_snake_case

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

    @staticmethod
    def map_into(type: Type[T], mapped: dict[Type, T]) -> T:
        snaked = dict(
            [(to_snake_case(v.__class__.__name__), v) for v in mapped.values()]
        )
        return type(**snaked)

    @staticmethod
    def map_into_all(type: Type[T], mapped: list[dict[Type, T]]) -> list[T]:
        return [TupleMapper.map_into(type, m) for m in mapped]

    class From:
        values: tuple

        def __init__(self, args: tuple) -> None:
            if args:
                tup: tuple = args
                self.values = tup
                return

            raise Exception("invalid args - please provide a tuple")

        def to(self, dest: Type[T], *multiType: Type[Any]) -> T:
            if len(multiType) <= 0:
                # try and get ctor parameter types - NOTE: this requires the ordering of parameters to match
                multiType = tuple([k for k in dest.__annotations__.values()])

            tup: tuple = tuple(*self.values)
            types = list(multiType)
            mapped = TupleMapper.map_multi(types, tup)
            v = TupleMapper.map_into(dest, mapped)
            return v

    class FromList:
        values: list[tuple]

        def __init__(self, args: list[tuple]) -> None:
            if isinstance(args, list):
                tups: list[tuple] = args
                self.values = tups
                return

            raise Exception("invalid args - please provide a list of tuples")

        def to(self, dest: Type[T], *multiType: Type[Any]) -> list[T]:
            if len(multiType) <= 0:
                # try and get ctor parameter types - NOTE: this requires the ordering of parameters to match the field order
                multiType = tuple([k for k in dest.__annotations__.values()])

            tups: list[tuple] = [tup for tup in self.values]
            types = list(multiType)
            mapped = TupleMapper.map_multi_all(types, tups)
            v = TupleMapper.map_into_all(dest, mapped)
            return v


# @dataclass
# class Me1:
#     id: int = 0
#     name: str = ""


# @dataclass
# class Me2:
#     id: int = 0
#     name: str = ""
#     date_of_birth: str = ""


# @dataclass
# class Dto:
#     me1: Me1 = Me1()
#     me2: Me2 = Me2()


## rely on Dto's field ordering for mapping multiple types (Me1 and Me2) into Dto
# dto = TupleMapper.From(
#     (1, "me-1", 2, "me-2", "2002-01-21")
# ).to(Dto)
# print(dto)

## pass Dto's field types in order for mapping multiple types (Me1 and Me2) into Dto
# dto = TupleMapper.From(
#     (1, "me-1", 2, "me-2", "2002-01-21")
# ).to(Dto, Me1, Me2)
# print(dto)


## rely on Dto's field ordering for mapping multiple types (Me1 and Me2) into Dto
# dto = TupleMapper.FromList(
#     [(1, "me-1", 2, "me-2", "2002-01-21"), (4, "me-4", 5, "me-5", "1998-06-14")]
# ).to(Dto)
# print(dto)

## pass Dto's field types in order for mapping multiple types (Me1 and Me2) into Dto
# dto = TupleMapper.FromList(
#     [(1, "me-1", 2, "me-2", "2002-01-21"), (4, "me-4", 5, "me-5", "1998-06-14")]
# ).to(Dto, Me1, Me2)
# print(dto)

## help(Dto)
