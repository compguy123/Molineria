import os
from sqlite3 import Connection, Cursor, Error, IntegrityError, connect
from contextlib import closing
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
from data.exceptions import (
    InvalidConnectionException,
    InvalidDatabaseException,
    MolineriaDataException,
    UniqueConstraintException,
)
import data.models as ModelTypes
from data.models import (
    Medication,
    Pharmacy,
    User,
    UserMedication,
    UserMedicationIntake,
    UserMedicationRefill,
)
from data.repositories import (
    BaseDataRepository,
    FakeDataRepository,
    MolineriaDataRepository,
)
from util.string_util import from_snake_case_to_pascal_case, is_null_or_whitespace


class BaseUnitOfWork(ABC):
    _database_name: str
    _conn: Connection
    _schema_sql_script: str
    _required_tables: list[str] = [
        "medication",
        "pharmacy",
        "user",
        "user_medication",
        "user_medication_refill",
        "user_medication_intake",
    ]
    _user_repo: BaseDataRepository[User] | None = None
    _medication_repo: BaseDataRepository[Medication] | None = None
    _pharmacy_repo: BaseDataRepository[Pharmacy] | None = None
    _user_medication_repo: BaseDataRepository[UserMedication] | None = None
    _user_medication_refill_repo: BaseDataRepository[UserMedicationRefill] | None = None
    _user_medication_intake_repo: BaseDataRepository[UserMedicationIntake] | None = None

    def __init__(self, database_name: str) -> None:
        if is_null_or_whitespace(database_name):
            raise InvalidConnectionException(
                "database_name cannot be null or whitespace."
            )

        if not database_name.endswith(".db"):
            raise InvalidConnectionException("database_name must be end with '.db'.")

        self._database_name = database_name

    def _print_value(self, category: str, value: Any) -> None:
        print(f"{__class__.__name__}.{__name__}(...) - {category} - ", value)

    def _ensure_connection_created(self) -> None:
        if (not hasattr(self, "_conn")) or (not self._conn):
            self._conn = connect(self._database_name)

    def _is_missing_any_tables(self, required_tables: list[str]) -> bool:
        self._ensure_connection_created()
        with closing(
            self._conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        ) as cursor:
            current_table_names: list[tuple[str]] = cursor.fetchall()
            for table in required_tables:
                if current_table_names.count((table,)) <= 0:
                    return True
            return False

    @staticmethod
    def get_model_type_by_table_name(table_name) -> type:
        model_name = from_snake_case_to_pascal_case(table_name)
        return getattr(ModelTypes, model_name)

    def __enter__(self) -> None:
        self.ensure_database_created()
        self._conn.__enter__()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._conn:
            self._conn.__exit__(exc_type, exc_value, traceback)
            self._conn.close()
        if self._user_repo:
            self._user_repo.close()
        if self._medication_repo:
            self._medication_repo.close()
        if self._pharmacy_repo:
            self._pharmacy_repo.close()
        if self._user_medication_repo:
            self._user_medication_repo.close()
        if self._user_medication_refill_repo:
            self._user_medication_refill_repo.close()
        if self._user_medication_intake_repo:
            self._user_medication_intake_repo.close()

    @abstractproperty
    def user_repo(self):
        pass

    @abstractproperty
    def medication_repo(self):
        pass

    @abstractproperty
    def pharmacy_repo(self):
        pass

    @abstractproperty
    def user_medication_repo(self):
        pass

    @abstractproperty
    def user_medication_refill_repo(self):
        pass

    @abstractproperty
    def user_medication_intake_repo(self):
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        pass

    @abstractmethod
    def ensure_database_created(self) -> None:
        pass

    @abstractmethod
    def execute_sql(self, sql: str, parameters: dict[str, Any]):
        cursor: Cursor
        try:
            with self._conn as conn:
                with closing(conn.execute(sql, parameters)) as cursor:
                    records: list[tuple] = cursor.fetchall()
                    return records
        except IntegrityError as err:
            self._print_value("EXEC SPEC ERROR -> UniqueConstraintException:", err)
            raise UniqueConstraintException(inner_exception=err)
        except Error as err:
            self._print_value("EXEC SPEC ERROR:", err)
            raise MolineriaDataException(inner_exception=err)


class FakeUnitOfWork(BaseUnitOfWork):
    def test_connection(self) -> bool:
        return super().test_connection()

    def ensure_database_created(self) -> None:
        return super().ensure_database_created()

    @property
    def user_repo(self):
        if not self._user_repo:
            self._user_repo = FakeDataRepository[User](
                connection=self._conn,
                table_name="user",
                select_cols="id,name,date_of_birth,comment",
            )
        return self._user_repo

    @property
    def medication_repo(self):
        if not self._medication_repo:
            self._medication_repo = FakeDataRepository[Medication](
                connection=self._conn,
                table_name="medication",
                select_cols="id,name,image_url,wiki_identifier",
            )
        return self._medication_repo

    @property
    def pharmacy_repo(self):
        if not self._pharmacy_repo:
            self._pharmacy_repo = FakeDataRepository[Pharmacy](
                connection=self._conn,
                table_name="pharmacy",
                select_cols="id,name,phone_number,location",
            )
        return self._pharmacy_repo

    @property
    def user_medication_repo(self):
        if not self._user_medication_repo:
            self._user_medication_repo = FakeDataRepository[UserMedication](
                connection=self._conn,
                table_name="user_medication",
                select_cols="id,user_id,rx_number,quantity,remaining_refills,weight_in_milligrams,filled_on,discard_on",
            )
        return self._user_medication_repo

    @property
    def user_medication_refill_repo(self):
        if not self._user_medication_refill_repo:
            self._user_medication_refill_repo = FakeDataRepository[
                UserMedicationRefill
            ](
                connection=self._conn,
                table_name="user_medication_refill",
                select_cols="id,user_medication_id,medication_id,pharmacy_id,prescribed_by,refilled_on,amount,comment",
            )
        return self._user_medication_refill_repo

    @property
    def user_medication_intake_repo(self):
        if not self._user_medication_intake_repo:
            self._user_medication_intake_repo = FakeDataRepository[
                UserMedicationIntake
            ](
                connection=self._conn,
                table_name="user_medication_intake",
                select_cols="id,user_medication_id,time,amount_in_milligrams,days_of_week",
            )
        return self._user_medication_intake_repo

    def execute_sql(self, sql: str, parameters: dict[str, Any]) -> list[tuple]:
        return []


class MolineriaUnitOfWork(BaseUnitOfWork):
    def __init__(self, database_name: str) -> None:
        super().__init__(database_name)
        # if schema_sql_script:
        # self._schema_sql_script = schema_sql_script
        # else:
        # figure out how to write testable code (maybe pass class to interact with file system?)
        schema_path = os.path.join(
            os.path.dirname(database_name),
            "scripts",
            "schema.sql",
        )
        with closing(open(schema_path)) as file:
            self._schema_sql_script = file.read()

    # maybe move to a database class and create database field in unit of work?
    def test_connection(self) -> bool:
        """Checks if a connection can be established and whether db can reply."""
        self._ensure_connection_created()

        with closing(self._conn.execute("SELECT 1")) as cursor:
            return cursor.fetchone()[0] == 1

    # maybe move to a database class and create database field in unit of work?
    def ensure_database_created(self) -> None:
        """Checks for any missing tables and creates them as needed.

        raises:
        - InvalidConnectionException - if connection couldn't be established.
        - InvalidDatabaseException - if failed to create missing tables.
        """
        self._ensure_connection_created()
        if not self.test_connection():
            raise InvalidConnectionException()

        if not self._is_missing_any_tables(self._required_tables):
            return

        with closing(self._conn.executescript(self._schema_sql_script)):
            if self._is_missing_any_tables(self._required_tables):
                raise InvalidDatabaseException(
                    f"we are missing one of the following tables: {self._required_tables}"
                )

    @property
    def user_repo(self):
        if not self._user_repo:
            self._ensure_connection_created()
            self._user_repo = MolineriaDataRepository[User](
                connection=self._conn,
                table_name=User().get_table_name(),
                select_cols=User().get_select_cols_str(),
            )
        return self._user_repo

    @property
    def medication_repo(self):
        if not self._medication_repo:
            self._ensure_connection_created()
            self._medication_repo = MolineriaDataRepository[Medication](
                connection=self._conn,
                table_name=Medication().get_table_name(),
                select_cols=Medication().get_select_cols_str(),
            )
        return self._medication_repo

    @property
    def pharmacy_repo(self):
        if not self._pharmacy_repo:
            self._ensure_connection_created()
            self._pharmacy_repo = MolineriaDataRepository[Pharmacy](
                connection=self._conn,
                table_name=Pharmacy().get_table_name(),
                select_cols=Pharmacy().get_select_cols_str(),
            )
        return self._pharmacy_repo

    @property
    def user_medication_repo(self):
        if not self._user_medication_repo:
            self._ensure_connection_created()
            self._user_medication_repo = MolineriaDataRepository[UserMedication](
                connection=self._conn,
                table_name=UserMedication().get_table_name(),
                select_cols=UserMedication().get_select_cols_str(),
            )
        return self._user_medication_repo

    @property
    def user_medication_refill_repo(self):
        if not self._user_medication_refill_repo:
            self._ensure_connection_created()
            self._user_medication_refill_repo = MolineriaDataRepository[
                UserMedicationRefill
            ](
                connection=self._conn,
                table_name=UserMedicationRefill().get_table_name(),
                select_cols=UserMedicationRefill().get_select_cols_str(),
            )
        return self._user_medication_refill_repo

    @property
    def user_medication_intake_repo(self):
        if not self._user_medication_intake_repo:
            self._ensure_connection_created()
            self._user_medication_intake_repo = MolineriaDataRepository[
                UserMedicationIntake
            ](
                connection=self._conn,
                table_name=UserMedicationIntake().get_table_name(),
                select_cols=UserMedicationIntake().get_select_cols_str(),
            )
        return self._user_medication_intake_repo

    def execute_sql(self, sql: str, parameters: dict[str, Any]):
        return super().execute_sql(sql, parameters)
