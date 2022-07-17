from typing import Optional


class MolineriaDataException(Exception):
    _message: str = None

    def __init__(self, message: Optional[str], *args: object) -> None:
        self._message = message
        super().__init__(*args)


class InvalidConnectionException(MolineriaDataException):
    def __init__(self, message: Optional[str], *args: object) -> None:
        if not message:
            message = "Failed to connect to database."
        super().__init__(message, *args)


class InvalidDatabaseException(MolineriaDataException):
    def __init__(self, message: Optional[str], *args: object) -> None:
        if not message:
            message = "Database is in an invalid state."
        super().__init__(message, *args)

