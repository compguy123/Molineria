from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar
from sqlite3 import Connection, Cursor, Error, IntegrityError
from contextlib import closing
import data.models as ModelTypes
from data.exceptions import MolineriaDataException, UniqueConstraintException
from data.models import BaseModel
from util.mapper import TupleMapper
from util.string import from_snake_case_to_pascal_case

TModel = TypeVar("TModel", bound=BaseModel)


class BaseDataRepository(ABC, Generic[TModel]):
    _conn: Connection
    _table_name: str = ""
    _select_cols: str = ""
    _type: type

    def __init__(
        self,
        connection: Connection,
        table_name: str,
        select_cols: str,
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

    def _get_model_type_by_table_name(self) -> Type[TModel]:
        try:
            model_name = from_snake_case_to_pascal_case(self._table_name)
            return getattr(ModelTypes, model_name)
        except AttributeError as err:
            self._print_value("DB MAPPING TO MODEL ERROR:", err)
            raise MolineriaDataException(
                f"Failed to get model type by table name '{self._table_name}'"
            )

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
            if len(records) <= 0:
                return None

            type = self._get_model_type_by_table_name()
            found_record: TModel = TupleMapper.map(type, records[0])
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
            if len(records) <= 0:
                return []

            type = self._get_model_type_by_table_name()
            found_records: list[TModel] = TupleMapper.map_all(type, records)
            return found_records

    @abstractmethod
    def create(self, record: TModel) -> TModel:
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
            with closing(self._conn.execute(sql, dict)) as cursor:
                id = cursor.lastrowid
                if not id:
                    raise MolineriaDataException("Failed to retreive ID after insert.")
                return self.get(id)
        except IntegrityError as err:
            self._print_value("CREATE ERROR -> UniqueConstraintException:", err)
            raise UniqueConstraintException(inner_exception=err)
        except Error as err:
            self._print_value("CREATE ERROR:", err)
            raise MolineriaDataException(inner_exception=err)

    @abstractmethod
    def update(self, record: TModel) -> TModel:
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
        try:
            with closing(self._conn.execute(sql, dict)):
                return self.get(record.id)
        except IntegrityError as err:
            self._print_value("UPDATE ERROR -> UniqueConstraintException:", err)
            raise UniqueConstraintException(inner_exception=err)
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
            with closing(self._conn.execute(sql, (id,))) as cursor:
                return cursor.rowcount == 1
        except Error as err:
            self._print_value("DELETE ERROR:", err)
            raise MolineriaDataException(inner_exception=err)


class FakeDataRepository(BaseDataRepository[TModel], Generic[TModel]):
    def __init__(
        self,
        connection: Connection,
        table_name: str,
        select_cols: str,
    ) -> None:
        super().__init__(connection, table_name, select_cols)

    def get(self, id: int) -> TModel | None:
        return None

    def get_all(self) -> list[TModel]:
        return []

    def create(self, record: TModel) -> TModel:
        return record

    def update(self, record: TModel) -> TModel:
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

    def create(self, record: TModel) -> TModel:
        return super().create(record)

    def update(self, record: TModel) -> TModel:
        return super().update(record)

    def delete(self, id: int) -> bool:
        return super().delete(id)
