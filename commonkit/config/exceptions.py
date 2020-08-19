# Classes


class VariableNameNotAllowed(Exception):
    """Raised when a disallowed variable is used in a config file."""

    def __init__(self, name, path, line=None):
        if line is not None:
            message = 'Variable name "%s" found in %s (line %s) is not allowed.' % (name, path, line)
        else:
            message = 'Variable name "%s" found in %s is not allowed.' % (name, path)

        super().__init__(message)
