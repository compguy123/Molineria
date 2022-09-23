from datetime import datetime, timedelta
from itertools import groupby
from typing import Any
from abc import ABC, abstractmethod
from data.models import (
    Medication,
    User,
    UserMedication,
    UserMedicationDetailDTO,
    UserMedicationDetailWithIntakeDTO,
    UserMedicationIntake,
)
from data.unit_of_work import BaseUnitOfWork
from util.mapper import TupleMapper


class BaseSpecification(ABC):
    def __init__(self, unit_of_work: BaseUnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    @abstractmethod
    def get_sql(self) -> tuple[str, dict[str, Any]]:
        pass

    @abstractmethod
    def execute(self):
        return self._unit_of_work.execute_sql(*self.get_sql())


class GetAllUsersOrderedSpec(BaseSpecification):
    def __init__(self, unit_of_work: BaseUnitOfWork) -> None:
        super().__init__(unit_of_work)

    def get_sql(self) -> tuple[str, dict[str, Any]]:
        u = User()
        sql = f"""
            SELECT {u.get_select_cols_str()}
            FROM {u.get_table_name()}
            ORDER BY name, id
            """
        return (sql, {})

    def execute(self):
        records = super().execute()
        found_records: list[User] = [User(*record) for record in records]
        return found_records


class GetAllUsersMedicationDetails(BaseSpecification):
    def __init__(self, unit_of_work: BaseUnitOfWork, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(unit_of_work)

    def get_sql(self) -> tuple[str, dict[str, Any]]:
        sql = f"""
            SELECT um.*, m.*
            FROM user_medication AS um
            INNER JOIN medication AS m ON m.id = um.medication_id
            WHERE um.user_id = @user_id
            ORDER BY m.name, um.id
            """
        return (sql, {"user_id": self.user_id})

    def execute(self):
        records = super().execute()
        return TupleMapper.FromList(records).to(UserMedicationDetailDTO)


class GetAllUsersMedicationDetailsWithIntakes(BaseSpecification):
    def __init__(self, unit_of_work: BaseUnitOfWork, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(unit_of_work)

    def get_sql(self) -> tuple[str, dict[str, Any]]:
        sql = f"""
            SELECT um.*, m.*, umi.*
            FROM user_medication AS um
            INNER JOIN medication AS m ON m.id = um.medication_id
            LEFT JOIN user_medication_intake AS umi ON umi.user_medication_id = um.id
            WHERE um.user_id = @user_id
            ORDER BY m.name, um.id
            """
        return (sql, {"user_id": self.user_id})

    def execute(self):
        records = super().execute()
        recs = TupleMapper.FromList(records).to(UserMedicationDetailWithIntakeDTO)

        def user_medication_id(umddwi: UserMedicationDetailWithIntakeDTO):
            return umddwi.user_medication.id

        def intake(umddwi: UserMedicationDetailWithIntakeDTO):
            return umddwi.user_medication_intake

        def next_intake(umddwi: UserMedicationDetailWithIntakeDTO):
            return umddwi.user_medication_intake.next_intake()

        result: list[
            tuple[UserMedicationDetailWithIntakeDTO, list[UserMedicationIntake]]
        ] = []

        for [k, v] in groupby(recs, key=user_medication_id):

            def target(umddwi: UserMedicationDetailWithIntakeDTO):
                return umddwi.user_medication.id == k

            head_intake = sorted(filter(target, recs), key=next_intake)[0]
            tail_intakes = list(map(intake, sorted(v, key=next_intake)))
            result.append((head_intake, tail_intakes))

        def next_intake_tup(
            t: tuple[UserMedicationDetailWithIntakeDTO, list[UserMedicationIntake]]
        ):
            return t[0].user_medication_intake.next_intake()

        r = sorted(result, key=next_intake_tup)
        return r

# class DeleteSpecifiedUserMeds(BaseSpecification):
#     def __init__(self, unit_of_work: BaseUnitOfWork, user_med_id: int) -> None:
#         self.user_med_id = user_med_id
#         super().__init__(unit_of_work)
#
#     def get_sql(self) -> tuple[str, dict[str, Any]]:
#         sql = f"""
#             SELECT um.*, m.*, umi.*
#             FROM user_medication AS um
#             INNER JOIN medication AS m ON m.id = um.medication_id
#             LEFT JOIN user_medication_intake AS umi ON umi.user_medication_id = um.id
#             WHERE um.user_id = @user_med_id
#             ORDER BY m.name, um.id
#             """
#         return (sql, {"user_med_id": self.user_med_id})
#
#     def execute(self):
#         records = super().execute()
#
#

## split tuples - (1,'asdf',...)[start : end : step]
# [tuple([x for x in range(1, 15)]) for _ in range(2)]
# tuple([x for x in range(1, 15)])[0:3:1]
