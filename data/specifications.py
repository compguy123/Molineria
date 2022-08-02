from typing import Any, Generic
from abc import ABC, abstractmethod
from data.models import User
from data.repositories import BaseDataRepository, TModel


class BaseSpecification(ABC, Generic[TModel]):
    _repo: BaseDataRepository[TModel]

    def __init__(self, repo: BaseDataRepository[TModel], *args) -> None:
        self._repo = repo

    @abstractmethod
    def get_sql(self) -> tuple[str, dict[str, Any]]:
        pass

    @abstractmethod
    def execute(self):
        return self._repo.execute_sql(*self.get_sql())


class GetAllUsersOrderedSpec(BaseSpecification[User]):
    def __init__(self, repo: BaseDataRepository[User], *args) -> None:
        super().__init__(repo, args)

    def get_sql(self) -> tuple[str, dict[str, Any]]:
        sql = f"""
            SELECT {self._repo._select_cols}
            FROM {self._repo._table_name}
            ORDER BY name, id
            """
        return (sql, {})

    def execute(self):
        return super().execute()
