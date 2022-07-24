class MolineriaDataException(Exception):
    _message: str | None = None
    _inner_exception: Exception | None = None

    def __init__(
        self,
        message: str | None = None,
        inner_exception: Exception | None = None,
        *args: object
    ) -> None:
        self._message = message
        self._inner_exception = inner_exception
        super().__init__(*args)


class InvalidConnectionException(MolineriaDataException):
    def __init__(
        self,
        message: str | None = None,
        inner_exception: Exception | None = None,
        *args: object
    ) -> None:
        if not message:
            message = "Failed to connect to database."
        self._message = message
        self._inner_exception = inner_exception
        super().__init__(message=message, *args)


class InvalidDatabaseException(MolineriaDataException):
    def __init__(
        self,
        message: str | None = None,
        inner_exception: Exception | None = None,
        *args: object
    ) -> None:
        if not message:
            message = "Database is in an invalid state."
        self._message = message
        self._inner_exception = inner_exception
        super().__init__(message=message, *args)
