# Exports

__all__ = (
    "DeeplyDisturbingError",
    "DoesNotCompute",
    "IMustBeMissingSomething",
    "ThisShouldNeverHappen",
    "YouShallNotPass",
)

# Classes


class DeeplyDisturbingError(Exception):
    """Indicates something is very (very) wrong with core, or "deep" functionality -- and we don't really know why."""
    pass


class DoesNotCompute(Exception):
    """Raised when a logical or mathematical operation has failed."""
    pass


class IMustBeMissingSomething(NotImplementedError):
    """Indicates an implementation is missing an attribute or method definition."""

    def __init__(self, class_name, attribute_name, method_name="auto"):
        """Issue the error.

        :param class_name: The name of the class with the missing attribute or method.
        :type class_name: str

        :param attribute_name: The name of the missing attribute.
        :type attribute_name: str

        :param method_name: The name (without the parentheses) of the method that calls the attribute. When set to
                            ``auto``, the method name becomes ``get_atttribute_name()`` -- whatever ``attribute_name``
                            may be.
        :type method_name: str

        """
        message = '"%s" must define "%s"' % (class_name, attribute_name)
        if method_name is not None:
            if method_name == "auto":
                method_name = "get_%s" % attribute_name

            message += ' or implement the "%s()" method' % method_name

        message += "."

        super().__init__(message)


class ThisShouldNeverHappen(Exception):
    """Indicates an application state that should never actually occur."""
    pass


class YouShallNotPass(Exception):
    """Indicates a conditional or other member has "passed" when it shouldn't.

    .. code-block:: py

        if some_condition:
            # ...
        elif some_other_condition:
            # ...
        else:
            raise YouShallNotPass("No valid condition found. I can't go on.")

    """
    pass
