from datetime import datetime, time
from json.encoder import JSONEncoder
from data.models import UserMedicationIntake as UMI

intakes = [
    UMI(id=1, days_of_week="tuesday"),
    UMI(id=2, days_of_week="monday", time=time(hour=4, minute=41)),
    UMI(id=3, days_of_week="friday", time=time(second=14)),
    UMI(id=4, days_of_week="wednesday", time=time(minute=2)),
    UMI(id=5, days_of_week="thursday,monday", time=time(hour=3)),
    UMI(id=6, days_of_week="monday", time=time(hour=21, minute=22, second=51)),
    UMI(id=7, days_of_week="sunday,tuesday", time=time(hour=11, minute=11, second=11)),
    UMI(id=8, days_of_week="wednesday,saturday", time=time(hour=6, minute=7, second=8)),
    UMI(id=9, days_of_week="thursday,friday"),
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
