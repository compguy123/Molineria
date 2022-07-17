import os
import sqlite3
from contextlib import closing
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Optional
from data.exceptions import InvalidConnectionException, InvalidDatabaseException
from data.models import Medication, Pharmacy, User, UserMedication, UserMedicationRefill
from data.repositories import BaseDataRepository, FakeDataRepository, UserDataRepository


class BaseUnitOfWork(ABC):
    _database_name: str = None
    _conn: sqlite3.Connection = None
    _schema_sql_script: str = None
    _required_tables: list[str] = [
        "medication",
        "pharmacy",
        "user",
        "user_medication",
        "user_medication_refill",
    ]
    _user_repo: BaseDataRepository[User] = None
    _medication_repo: BaseDataRepository[Medication] = None
    _pharmacy_repo: BaseDataRepository[Pharmacy] = None
    _user_medication_repo: BaseDataRepository[UserMedication] = None
    _user_medication_refill_repo: BaseDataRepository[UserMedicationRefill] = None

    def __init__(self, database_name: str) -> None:
        if not database_name or not database_name.strip():
            raise InvalidConnectionException("database_name cannot be null or empty.")

        if not database_name.endswith(".db") or not os.path.exists(database_name):
            raise InvalidConnectionException(
                "database_name must be a valid path to a '.db' file."
            )

        self._database_name = database_name
        # self._schema_sql_script = schema_sql_script

    def _print_value(self, category: str, value: Any) -> None:
        print(f"{__class__.__name__}.{__name__}(...) - {category} - ", value)

    def _ensure_connection_created(self) -> None:
        if not self._conn:
            self._conn = sqlite3.connect(self._database_name)

    def _is_missing_any_tables(self, required_tables: list[str]) -> bool:
        with closing(
            self._conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        ) as cursor:
            current_table_names = cursor.fetchall()
            for table in required_tables:
                if current_table_names.count((table,)) <= 0:
                    return True

    def __enter__(self) -> None:
        self.ensure_database_created()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._conn:
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

    @abstractproperty
    def user_repo(self) -> BaseDataRepository[User]:
        pass

    @abstractproperty
    def medication_repo(self) -> BaseDataRepository[Medication]:
        pass

    @abstractproperty
    def pharmacy_repo(self) -> BaseDataRepository[Pharmacy]:
        pass

    @abstractproperty
    def user_medication_repo(self) -> BaseDataRepository[UserMedication]:
        pass

    @abstractproperty
    def user_medication_refill_repo(
        self,
    ) -> BaseDataRepository[UserMedicationRefill]:
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        pass

    @abstractmethod
    def ensure_database_created(self) -> None:
        pass


class FakeUnitOfWork(BaseUnitOfWork):
    def test_connection(self) -> bool:
        return super().test_connection()

    def ensure_database_created(self) -> None:
        return super().ensure_database_created()

    @property
    def user_repo(self) -> FakeDataRepository[User]:
        if not self._user_repo:
            self._user_repo = FakeDataRepository[User](self._conn)
        return self._user_repo

    @property
    def medication_repo(self) -> FakeDataRepository[Medication]:
        if not self._medication_repo:
            self._medication_repo = FakeDataRepository[Medication](self._conn)
        return self._medication_repo

    @property
    def pharmacy_repo(self) -> FakeDataRepository[Pharmacy]:
        if not self._pharmacy_repo:
            self._pharmacy_repo = FakeDataRepository[Pharmacy](self._conn)
        return self._pharmacy_repo

    @property
    def user_medication_repo(self) -> FakeDataRepository[UserMedication]:
        if not self._user_medication_repo:
            self._user_medication_repo = FakeDataRepository[UserMedication](self._conn)
        return self._user_medication_repo

    @property
    def user_medication_refill_repo(
        self,
    ) -> FakeDataRepository[UserMedicationRefill]:
        if not self._user_medication_refill_repo:
            self._user_medication_refill_repo = FakeDataRepository[
                UserMedicationRefill
            ](self._conn)
        return self._user_medication_refill_repo


class MolineriaUnitOfWork(BaseUnitOfWork):
    def __init__(self, database_name: str) -> None:
        super().__init__(database_name)
        # if schema_sql_script:
        # self._schema_sql_script = schema_sql_script
        # else:
        # figure out how to write testable code (maybe pass class to interact with file system?)
        schema_path = os.path.join(
            os.path.dirname(database_name), "scripts", "schema.sql"
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
    def user_repo(self) -> UserDataRepository:
        if not self._user_repo:
            self._ensure_connection_created()
            self._user_repo = UserDataRepository(self._conn)
        return self._user_repo

    @property
    def medication_repo(self) -> BaseDataRepository[Medication]:
        if not self._medication_repo:
            self._ensure_connection_created()
            self._medication_repo = BaseDataRepository[Medication](self._conn)
        return self._medication_repo

    @property
    def pharmacy_repo(self) -> BaseDataRepository[Pharmacy]:
        if not self._pharmacy_repo:
            self._ensure_connection_created()
            self._pharmacy_repo = BaseDataRepository[Pharmacy](self._conn)
        return self._pharmacy_repo

    @property
    def user_medication_repo(self) -> BaseDataRepository[UserMedication]:
        if not self._user_medication_repo:
            self._ensure_connection_created()
            self._user_medication_repo = BaseDataRepository[UserMedication](self._conn)
        return self._user_medication_repo

    @property
    def user_medication_refill_repo(
        self,
    ) -> BaseDataRepository[UserMedicationRefill]:
        if not self._user_medication_refill_repo:
            self._ensure_connection_created()
            self._user_medication_refill_repo = BaseDataRepository[
                UserMedicationRefill
            ](self._conn)
        return self._user_medication_refill_repo
