from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from sqlite3 import Connection, Cursor, IntegrityError
from contextlib import closing
from data.exceptions import MolineriaDataException
from data.models import BaseModel, User

TModel = TypeVar("TModel", bound=BaseModel)


class BaseDataRepository(ABC, Generic[TModel]):
    _conn: Connection = None

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def close(self):
        if self._conn:
            self._conn.close()

    def _print_value(self, category: str, value: Any) -> None:
        print(f"{__class__.__name__}.{__name__}(...) - {category} - ", value)

    @abstractmethod
    def get(self, id: int) -> TModel | None:
        if id <= 0:
            raise MolineriaDataException("id must be > 0.")

    @abstractmethod
    def get_all(self, predicate: Optional[TModel]) -> list[TModel]:
        if predicate and not callable(predicate):
            raise MolineriaDataException("WHAT? func with no brim???")

    @abstractmethod
    def create(self, record: TModel) -> TModel | None:
        if record is None or record.id != 0:
            raise MolineriaDataException(
                "record cannot be None and record.id must be == 0."
            )

    @abstractmethod
    def update(self, record: TModel) -> TModel | None:
        if record is None or record.id <= 0:
            raise MolineriaDataException(
                "record cannot be None and record.id must be > 0."
            )

    @abstractmethod
    def delete(self, id: int) -> bool:
        if id <= 0:
            raise MolineriaDataException("id must be > 0.")


class FakeDataRepository(BaseDataRepository[TModel], Generic[TModel]):
    def get(self, id: int) -> TModel | None:
        return super().get(id)

    def get_all(self, predicate: Optional[TModel]) -> list[TModel]:
        return super().get_all(predicate)

    def create(self, record: TModel) -> TModel | None:
        return super().create(record)

    def update(self, record: TModel) -> TModel | None:
        return super().update(record)

    def delete(self, id: int) -> bool:
        return super().delete(id)


class UserDataRepository(BaseDataRepository[User]):
    _select_cols = "id, name, date_of_birth, comment"

    def _user_to_paramters(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "date_of_birth": user.date_of_birth,
            "comment": user.comment,
        }

    def __init__(self, connection: Connection) -> None:
        super().__init__(connection)

    def get(self, id: int) -> User | None:
        super().get(id)
        sql = f"""
            SELECT {self._select_cols} FROM user
            WHERE id == ?
            LIMIT 1;
            """
        cursor: Cursor
        with closing(self._conn.execute(sql, (id,))) as cursor:
            records: list[tuple[int, str, str, str]] = cursor.fetchall()
            if len(records) >= 0:
                return User.create(records[0])

    # either translate predicate to sql
    # or use something like specification pattern?
    # or create methods only for user repo?
    def get_all(self, predicate: Optional[User]) -> list[User]:
        super().get_all(predicate)
        sql = f"""
            SELECT {self._select_cols} FROM user
            ORDER BY id;
            """
        cursor: Cursor
        with closing(self._conn.execute(sql)) as cursor:
            records: list[User] = cursor.fetchall()
            if len(records) >= 0:
                return User.create(records[0])

    def create(self, record: User) -> User | None:
        super().create(record)
        sql = f"""
            INSERT INTO user
                    (name, date_of_birth, comment)
                VALUES
                    (@name, @date_of_birth, @comment);
            """
        cursor: Cursor
        try:
            with self._conn:
                parameters = self._user_to_paramters(record)
                with closing(self._conn.execute(sql, parameters)) as cursor:
                    self._conn.commit()
                    return self.get(cursor.lastrowid)
        except IntegrityError as ex:
            self._print_value("ERROR:", ex)

    def update(self, record: User) -> User | None:
        super().update(record)
        sql = f"""
            UPDATE user SET
                name = @name
                ,date_of_birth = @date_of_birth
                ,comment = @comment
            WHERE id = @id;
            """
        cursor: Cursor
        try:
            with self._conn:
                parameters = self._user_to_paramters(record)
                with closing(self._conn.executemany(sql, parameters)) as cursor:
                    records: list[User] = cursor.fetchall()
                    if len(records) >= 0:
                        return User.create(records[0])
        except IntegrityError as ex:
            self._print_value("ERROR:", ex)

    def delete(self, id: int) -> bool:
        super().delete(id)
        sql = f"""
            DELETE FROM user
            WHERE id = ?;
            """
        cursor: Cursor
        try:
            with self._conn:
                with closing(self._conn.execute(sql, (id,))) as cursor:
                    return cursor.rowcount == 1
        except IntegrityError as ex:
            self._print_value("ERROR:", ex)
