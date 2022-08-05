from datetime import datetime, time
from json.encoder import JSONEncoder
from typing import Type, TypeVar
from data.models import UserMedicationIntake as UMI

T = TypeVar("T")


def create_factory(type: Type[T]):
    i = [0]

    def create(days_of_week: str, time: time | None = None) -> T:
        i[0] = i[0] + 1
        return type(
            **{
                "id": i[0],
                "days_of_week": days_of_week,
                "time": time.isoformat() if time else "",
            }
        )

    return create


creator = create_factory(UMI)
intakes = [
    creator("tuesday"),
    creator("monday", time(hour=4, minute=41)),
    creator("friday", time(second=14)),
    creator("wednesday", time(minute=2)),
    creator("thursday,monday", time(hour=3)),
    creator("monday", time(hour=21, minute=22, second=51)),
    creator("sunday,tuesday", time(hour=11, minute=11)),
    creator("wednesday,saturday", time(hour=6, minute=7)),
    creator("thursday,friday"),
]


def format_intakes(intakes: list[UMI]):
    return list(
        map(
            lambda x: f"[{x.id}] {x.next_intake()} ({x.next_intake_as_target().remaining_short_humanized})",
            intakes,
        )
    )


now = datetime.now()
json_serializer = JSONEncoder(indent=4)

targets = format_intakes(intakes)
print(f"now:     {now:%Y-%m-%d %H:%M:%S}")
print(f"intakes: {json_serializer.encode(targets)}")

intakes.sort(key=UMI.next_intake)

targets: list[str] = format_intakes(intakes)
print(f"now:     {now:%Y-%m-%d %H:%M:%S}")
print(f"sorted intakes: {json_serializer.encode(targets)}")
