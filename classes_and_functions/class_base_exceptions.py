class ParseError(Exception):
    """Base class for other exceptions."""
    pass


class InvalidDepartment(ParseError):
    """An invalid department code was entered."""
    pass


class InvalidCourse(ParseError):
    """An invalid course code was entered."""
    pass


class WorkingScheduleNotFound(Exception):
    """Working schedule was unable to be made, due to number of classes or availability."""
    pass
