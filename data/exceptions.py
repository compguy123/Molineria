class MolineriaDataException(Exception):
    _message: str | None = None
    _inner_exception: Exception | None = None

    def __init__(
        self,
        message: str | None = None,
        inner_exception: Exception | None = None,
        *args: object,
    ) -> None:
        self._message = message
        self._inner_exception = inner_exception
        super().__init__(*args)


class InvalidConnectionException(MolineriaDataException):
    def __init__(
        self,
        message: str | None = "Failed to connect to database.",
        inner_exception: Exception | None = None,
        *args: object,
    ) -> None:
        super().__init__(message=message, inner_exception=inner_exception, *args)


class InvalidDatabaseException(MolineriaDataException):
    def __init__(
        self,
        message: str | None = "Database is in an invalid state.",
        inner_exception: Exception | None = None,
        *args: object,
    ) -> None:
        super().__init__(message=message, inner_exception=inner_exception, *args)


class UniqueConstraintException(MolineriaDataException):
    _error_type: str | None = None
    _field_name: str | None = None

    def __init__(
        self,
        field_name: str | None = None,
        message: str | None = None,
        inner_exception: Exception | None = None,
        *args: object,
    ) -> None:
        if (
            not message
            and inner_exception
            and inner_exception.__class__.__name__ == "IntegrityError"
        ):
            type: str
            field: str
            type, field = [e.strip() for e in inner_exception.args[0].split(":")]

            self._error_type = type
            if field_name:
                self._field_name = field_name
            else:
                self._field_name = field

            message = f"{self._error_type}: {self._field_name}"

        super().__init__(message=message, inner_exception=inner_exception, *args)
