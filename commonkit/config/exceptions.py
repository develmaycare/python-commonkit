# Classes


class VariableNameNotAllowed(Exception):
    """Raised when a disallowed variable is used in a config file."""

    def __init__(self, name, path, line=None):
        """Initialize the exception.

        :param name: The name of the variable.
        :type name: str

        :param path: The path of the configuration file.
        :type path: str

        :param line: The line number in the configuration file where the variable is defined.
        :type line: int

        """
        if line is not None:
            message = 'Variable name "%s" found in %s (line %s) is not allowed.' % (name, path, line)
        else:
            message = 'Variable name "%s" found in %s is not allowed.' % (name, path)

        super().__init__(message)
