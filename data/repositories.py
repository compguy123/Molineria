from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from sqlite3 import Connection, Cursor, Error
from contextlib import closing
import data
from data.exceptions import MolineriaDataException
from data.models import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class BaseDataRepository(ABC, Generic[TModel]):
    _conn: Connection | None = None
    _table_name: str | None = None
    _select_cols: str | None = None
    _type: type | None = None

    def __init__(
        self,
        connection: Connection | None,
        table_name: str | None,
        select_cols: str | None,
    ) -> None:
        self._conn = connection
        self._table_name = table_name
        self._select_cols = select_cols
        self._type = self._get_model_type_by_table_name()

    def close(self):
        if self._conn:
            self._conn.close()

    def _print_value(self, category: str, value: Any) -> None:
        print(f"{__class__.__name__}.{__name__}(...) - {category} - ", value)

    def _from_snake_case_to_pascal_case(self, value: str) -> str:
        return value.replace("_", " ").title().replace(" ", "")

    def _get_model_type_by_table_name(self) -> type:
        try:
            model_name = self._from_snake_case_to_pascal_case(self._table_name)
            return getattr(data.models, model_name)
        except AttributeError as err:
            self._print_value("DB MAPPING TO MODEL ERROR:", err)
            return None

    @abstractmethod
    def get(self, id: int) -> TModel | None:
        if id <= 0:
            raise MolineriaDataException("id must be > 0.")
        sql = f"""
            SELECT {self._select_cols} FROM {self._table_name}
            WHERE id == ?
            LIMIT 1;
            """
        cursor: Cursor
        with closing(self._conn.execute(sql, (id,))) as cursor:
            records: list[tuple] = cursor.fetchall()
            if len(records) > 0:
                found_record = self._get_model_type_by_table_name()(*records[0])
                return found_record

    @abstractmethod
    def get_all(self) -> list[TModel]:
        sql = f"""
            SELECT {self._select_cols} FROM {self._table_name}
            ORDER BY id;
            """
        cursor: Cursor
        with closing(self._conn.execute(sql)) as cursor:
            records: list[tuple] = cursor.fetchall()
            if len(records) > 0:
                found_records = [
                    self._get_model_type_by_table_name()(*record) for record in records
                ]
                return found_records

    @abstractmethod
    def create(self, record: TModel) -> TModel | None:
        if record is None or record.id != 0:
            raise MolineriaDataException(
                "record cannot be None and record.id must be == 0."
            )
        dict = vars(record)
        keys = list(filter(lambda k: k != "id", dict.keys()))
        column_names = ", ".join([k for k in keys])
        parameter_names = ", ".join([f"@{k}" for k in keys])
        sql = f"""
            INSERT INTO {self._table_name}
                    ({column_names})
                VALUES
                    ({parameter_names});
            """
        cursor: Cursor
        try:
            with self._conn as conn:
                with closing(conn.execute(sql, dict)) as cursor:
                    return self.get(cursor.lastrowid)
        except Error as err:
            self._print_value("CREATE ERROR:", err)
            raise MolineriaDataException(inner_exception=err)

    @abstractmethod
    def update(self, record: TModel) -> TModel | None:
        if record is None or record.id <= 0:
            raise MolineriaDataException(
                "record cannot be None and record.id must be > 0."
            )
        dict = vars(record)
        keys = list(filter(lambda k: k != "id", dict.keys()))
        names_parameters = "\n\t,".join([f"{k} = @{k}" for k in keys])
        # don't need to generate where clause because we assume that all records inherit BaseModel
        sql = f"""
            UPDATE {self._table_name} SET
            {names_parameters}
            WHERE id = @id;
            """
        cursor: Cursor
        try:
            with self._conn as conn:
                with closing(conn.execute(sql, dict)) as cursor:
                    return self.get(record.id)
        except Error as err:
            self._print_value("UPDATE ERROR:", err)
            raise MolineriaDataException(inner_exception=err)

    @abstractmethod
    def delete(self, id: int) -> bool:
        if id <= 0:
            raise MolineriaDataException("id must be > 0.")
        sql = f"""
            DELETE FROM {self._table_name}
            WHERE id = ?;
            """
        cursor: Cursor
        try:
            with self._conn as conn:
                with closing(conn.execute(sql, (id,))) as cursor:
                    return cursor.rowcount == 1
        except Error as err:
            self._print_value("DELETE ERROR:", err)
            raise MolineriaDataException(inner_exception=err)


class FakeDataRepository(BaseDataRepository[TModel], Generic[TModel]):
    def __init__(
        self,
        connection: Connection | None,
        table_name: str | None,
        select_cols: str | None,
    ) -> None:
        super().__init__(connection, table_name, select_cols)

    def get(self, id: int) -> TModel | None:
        return None

    def get_all(self) -> list[TModel]:
        return []

    def create(self, record: TModel) -> TModel | None:
        return record

    def update(self, record: TModel) -> TModel | None:
        return record

    def delete(self, id: int) -> bool:
        return True


class MolineriaDataRepository(BaseDataRepository[TModel], Generic[TModel]):
    def __init__(
        self,
        connection: Connection,
        table_name: str,
        select_cols: str,
    ) -> None:
        super().__init__(connection, table_name, select_cols)

    def get(self, id: int) -> TModel | None:
        return super().get(id)

    def get_all(self) -> list[TModel]:
        return super().get_all()

    def create(self, record: TModel) -> TModel | None:
        return super().create(record)

    def update(self, record: TModel) -> TModel | None:
        return super().update(record)

    def delete(self, id: int) -> bool:
        return super().delete(id)
