from __future__ import annotations
from abc import ABC
from datetime import date


class BaseModel(ABC):
    _id: int = 0

    @property
    def id(self) -> int:
        return self._id


class User(BaseModel):
    def __init__(
        self, name: str, date_of_birth: date | None, comment: str | None
    ) -> None:
        self._name = name
        self._date_of_birth = date_of_birth
        self._comment = comment

    @staticmethod
    def create(tuple: tuple[int, str, str, str]) -> User:
        user = User(tuple[1], tuple[2], tuple[3])
        user._id = tuple[0]
        return user

    @property
    def name(self) -> str:
        return self._name

    @property
    def date_of_birth(self) -> date:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth) -> None:
        self._date_of_birth = date_of_birth

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment) -> None:
        self._comment = comment


class Medication(BaseModel):
    def __init__(
        self, name: str, image_url: str | None, wiki_identifier: str | None
    ) -> None:
        self._name = name
        self._image_url = image_url
        self._wiki_identifier = wiki_identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def image_url(self) -> str | None:
        return self._image_url

    @image_url.setter
    def image_url(self, image_url: str) -> None:
        self._image_url = image_url

    @property
    def wiki_identifier(self) -> str | None:
        return self._wiki_identifier

    @wiki_identifier.setter
    def set_wiki_identifier(self, wiki_identifier: str) -> None:
        self._wiki_identifier = wiki_identifier


class Pharmacy(BaseModel):
    def __init__(
        self, name: str, phone_number: str | None, location: str | None
    ) -> None:
        self._name = name
        self._phone_number = phone_number
        self._location = location

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str) -> None:
        self._phone_number = phone_number

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, location: str) -> None:
        self._location = location


class UserMedication(BaseModel):
    def __init__(
        self,
        user_id: int,
        medication_id: int,
        rx_number: str,
        quantity: int,
        remaining_refills: int | None,
        weight_in_milligrams: float | None,
        filled_on: date | None,
        discard_on: date | None,
    ) -> None:
        self._user_id = user_id
        self._medication_id = medication_id
        self._rx_number = rx_number
        self._quantity = quantity
        self._remaining_refills = remaining_refills
        self._weight_in_milligrams = weight_in_milligrams
        self._filled_on = filled_on
        self._discard_on = discard_on

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def rx_number(self) -> int:
        return self._rx_number

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        self._quantity = quantity

    @property
    def remaining_refills(self) -> int | None:
        return self._remaining_refills

    @remaining_refills.setter
    def remaining_refills(self, remaining_refills: int) -> None:
        self._remaining_refills = remaining_refills

    @property
    def weight_in_milligrams(self) -> float | None:
        return self._weight_in_milligrams

    @weight_in_milligrams.setter
    def weight_in_milligrams(self, weight_in_milligrams: float) -> None:
        self._weight_in_milligrams = weight_in_milligrams

    @property
    def filled_on(self) -> date | None:
        return self._filled_on

    @filled_on.setter
    def filled_on(self, filled_on: date) -> None:
        self._filled_on = filled_on

    @property
    def discard_on(self) -> date | None:
        return self._discard_on

    @discard_on.setter
    def discard_on(self, discard_on: date) -> None:
        self._discard_on = discard_on


class UserMedicationRefill(BaseModel):
    def __init__(
        self,
        user_medication_id: int,
        medication_id: int,
        pharmacy_id: int,
        prescribed_by: str | None,
        refilled_on: date | None,
        amount: int | None,
        comment: str | None,
    ) -> None:
        self._user_medication_id = user_medication_id
        self._medication_id = medication_id
        self._pharmacy_id = pharmacy_id
        self._prescribed_by = prescribed_by
        self._refilled_on = refilled_on
        self._amount = amount
        self._comment = comment

    @property
    def user_medication_id(self) -> str:
        return self._user_medication_id

    @property
    def medication_id(self) -> str:
        return self._medication_id

    @property
    def pharmacy_id(self) -> str:
        return self._pharmacy_id

    @property
    def prescribed_by(self) -> str:
        return self._prescribed_by

    @prescribed_by.setter
    def prescribed_by(self, prescribed_by: str) -> None:
        self._prescribed_by = prescribed_by

    @property
    def refilled_on(self) -> date | None:
        return self._refilled_on

    @refilled_on.setter
    def refilled_on(self, refilled_on: date) -> None:
        self._refilled_on = refilled_on

    @property
    def amount(self) -> int | None:
        return self._amount

    @amount.setter
    def amount(self, amount: int) -> None:
        self._amount = amount

    @property
    def comment(self) -> str | None:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self._comment = comment
