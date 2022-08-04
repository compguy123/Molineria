from typing import Any
from abc import ABC, abstractmethod
from data.models import (
    Medication,
    User,
    UserMedication,
    UserMedicationDetailDTO,
)
from data.unit_of_work import BaseUnitOfWork


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
        result: list[UserMedicationDetailDTO] = []

        for record_tuple in records:
            step_len = 1
            starting_point = 0
            next_stopping_point = len(vars(UserMedication()))

            tup = record_tuple[starting_point:next_stopping_point:step_len]
            user_medication = UserMedication(*tup)  # type: ignore

            starting_point = next_stopping_point
            next_stopping_point = next_stopping_point + len(vars(Medication()))

            tup = record_tuple[starting_point:next_stopping_point:step_len]
            medication = Medication(*tup)  # type: ignore

            rec = UserMedicationDetailDTO(
                medication=medication, user_medication=user_medication
            )
            result.append(rec)

        return result


## split tuples - (1,'asdf',...)[start : end : step]
# [tuple([x for x in range(1, 15)]) for _ in range(2)]
# tuple([x for x in range(1, 15)])[0:3:1]
