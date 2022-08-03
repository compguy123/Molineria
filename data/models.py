from abc import ABC
from dataclasses import dataclass
from datetime import time, date
from enum import Enum

from util.string_util import to_snake_case


class DayOfWeek(Enum):
    Monday = "monday"
    Tuesday = "tuesday"
    Wednesday = "wednesday"
    Thursday = "thursday"
    Friday = "friday"
    Saturday = "saturday"
    Sunday = "sunday"


@dataclass
class BaseModel(ABC):
    id: int = 0

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
    comment: str | None = None

    @property
    def age(self):
        if not self.date_of_birth:
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
    time: time = time.min
    amount_in_milligrams: float = 0
    days_of_week: str = ""

    def has_day_of_week(self, target: DayOfWeek) -> bool:
        if not self.days_of_week or not target:
            return False
        days_of_week_list = self.days_of_week.lower().split(",")
        return any(filter(lambda d: d == target.value, days_of_week_list))


# <time>.strftime("%I:%M:%S") -> 12 hr format
### get field names in order
# ",".join([k for k in vars(UserMedicationIntake()).keys()])
