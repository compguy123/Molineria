from abc import ABC
from dataclasses import dataclass
from datetime import date


@dataclass
class BaseModel(ABC):
    id: int = 0


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


### get field names in order
# ",".join([k for k in vars(UserMedicationRefill()).keys()])
