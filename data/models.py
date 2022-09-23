from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, time, date, timedelta
from enum import Enum
from typing import Any, Type
from util.models import TargetDatetime
from util.string import to_snake_case


class DayOfWeek(Enum):
    Monday = "monday"
    Tuesday = "tuesday"
    Wednesday = "wednesday"
    Thursday = "thursday"
    Friday = "friday"
    Saturday = "saturday"
    Sunday = "sunday"

    @staticmethod
    def __get_mapping_from_iso():
        return {
            1: DayOfWeek.Monday,
            2: DayOfWeek.Tuesday,
            3: DayOfWeek.Wednesday,
            4: DayOfWeek.Thursday,
            5: DayOfWeek.Friday,
            6: DayOfWeek.Saturday,
            7: DayOfWeek.Sunday,
        }

    @staticmethod
    def __get_mapping_to_iso():
        from_mapping = DayOfWeek.__get_mapping_from_iso()
        k = from_mapping.keys()
        v = from_mapping.values()
        return dict(zip(v, k))

    def toisoweekday(self):
        mapping = DayOfWeek.__get_mapping_to_iso()
        return mapping[self]

    @staticmethod
    def fromisoweekday(isoweekday: int):
        mapping = DayOfWeek.__get_mapping_from_iso()
        return mapping[isoweekday]

    @staticmethod
    def fromdate(date: date):
        return DayOfWeek.fromisoweekday(date.isoweekday())

    @staticmethod
    def fromdatetime(datetime: datetime):
        return DayOfWeek.fromisoweekday(datetime.isoweekday())

    @staticmethod
    def parse(value: str):
        return DayOfWeek(value.strip().lower())


@dataclass
class BaseModel(ABC):
    id: int = 0

    def __init__(self, id: int) -> None:
        self.id = id
        self.on_create()
        super().__init__()

    def on_create(self):
        pass

    def get_select_cols(self):
        return list(map(lambda x: x, vars(self)))

    def get_select_cols_str(self):
        return ",".join(self.get_select_cols())

    def get_table_name(self):
        return to_snake_case(self.__class__.__name__)


@dataclass
class User(BaseModel):
    name: str = ""
    date_of_birth: date | None = None
    email: str | None = None
    last_login_date: date | None = None

    @property
    def age(self):
        if not self.date_of_birth or not isinstance(self.date_of_birth, date):
            return None
        return date.today().year - self.date_of_birth.year


@dataclass
class Medication(BaseModel):
    name: str = ""
    image_url: str | None = None
    wiki_identifier: str | None = None


@dataclass
class Pharmacy(BaseModel):
    name: str = ""
    phone_number: str | None = None
    location: str | None = None


@dataclass
class UserMedication(BaseModel):
    user_id: int = 0
    medication_id: int = 0
    rx_number: str = ""
    quantity: int = 0
    remaining_refills: int | None = None
    weight_in_milligrams: float | None = None
    total_weight_in_milligrams: float | None = None
    filled_on: date | None = None
    discard_on: date | None = None


@dataclass
class UserMedicationRefill(BaseModel):
    user_medication_id: int = 0
    pharmacy_id: int = 0
    prescribed_by: str | None = None
    refilled_on: date | None = None
    amount_in_milligrams: float | None = None
    comment: str | None = None


@dataclass
class UserMedicationIntake(BaseModel):
    user_medication_id: int = 0
    time: str = ""
    amount_in_milligrams: float = 0
    days_of_week: str = ""

    def has_day_of_week(self, target: DayOfWeek) -> bool:
        if not self.days_of_week or not target:
            return False
        days_of_week_list = self.days_of_week.lower().split(",")
        return any(filter(lambda d: d == target.value, days_of_week_list))

    def try_add_day_of_week(self, day_of_week: DayOfWeek) -> bool:
        if not self.has_day_of_week(day_of_week):
            self.days_of_week = f"{self.days_of_week},{day_of_week.value}"
            return True
        return False

    def try_remove_day_of_week(self, day_of_week: DayOfWeek) -> bool:
        if not self.has_day_of_week(day_of_week):
            return False
        days_of_week_list = self.days_of_week.lower().split(",")
        days_of_week_list.remove(day_of_week.value)
        self.days_of_week = ",".join(days_of_week_list)
        return True

    def next_intake(self):
        if self.id is None:
            return datetime.now()

        current = datetime.now()
        my_time = (
            time.fromisoformat(self.time)
            if self.time and isinstance(self.time, str)
            else time.min
        )
        current_day_of_week = DayOfWeek.fromdatetime(current)
        has_day_of_week = self.has_day_of_week(current_day_of_week)

        while not has_day_of_week or (has_day_of_week and my_time < current.time()):
            current = (current + timedelta(days=1)).date()
            current = datetime.combine(current, my_time)
            current_day_of_week = DayOfWeek.fromdatetime(current)
            has_day_of_week = self.has_day_of_week(current_day_of_week)

        target = datetime.combine(current, my_time)
        return target

    def next_intake_as_target(self) -> TargetDatetime:
        return TargetDatetime(self.next_intake())


@dataclass
class BaseDTO(ABC):
    # maybe we can use this for mapping or building queries?
    @abstractmethod
    def get_field_types(self) -> list[Type[Any]]:
        return [v for v in self.__annotations__.values()]


@dataclass
class UserMedicationDetailDTO(BaseDTO):
    user_medication: UserMedication
    medication: Medication

    def get_field_types(self):
        return super().get_field_types()


@dataclass
class UserMedicationDetailWithIntakeDTO(BaseDTO):
    user_medication: UserMedication
    medication: Medication
    user_medication_intake: UserMedicationIntake

    def get_field_types(self):
        return super().get_field_types()


# <time>.strftime("%I:%M:%S") -> 12 hr format
### get field names in order
# ",".join([k for k in vars(UserMedicationIntake()).keys()])
