class ParseError(Exception):
    """Base class for other exceptions."""
    pass


class InvalidDepartment(ParseError):
    """An invalid department code was entered."""
    pass


class InvalidCourse(ParseError):
    """An invalid course code was entered."""
    pass
