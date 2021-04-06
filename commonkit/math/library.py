# Imports

from functools import reduce
import operator
import statistics

# Exports

__all__ = (
    "add",
    "average",
    "difference",
    "factors_of",
    "is_prime",
    "median",
    "percentage",
    "product",
)

# Functions


def add(values, base=None):
    """Add values together.

    :param values: An iterable of values to be added. Unlike ``sum``, these may be of different types.

    :param base: Applied to the beginning of the calculation.
    :type base: int

    """
    if base is None:
        return reduce(operator.add, values)

    return reduce(operator.add, values, base)


def average(values, lazy=False):
    """Calculate the average of a given number of values.

    :param values: The values to be averaged.
    :type values: list | tuple

    :param lazy: When ``True`` zeroes (0) are removed before averaging.
    :type lazy: bool

    :rtype: float

    Ever get tired of creating a try/except for zero division? I do.

    .. code-block:: python

        from commonkit.utils import average

        values = [1, 2, 3, 4, 5]
        print(average(values))

    """
    if lazy:
        values = [i for i in values if i != 0]

    try:
        return float(sum(values) / len(values))
    except ZeroDivisionError:
        return 0.0


def difference(value1, value2, absolute=True, precision=2):
    """Get the difference between two numbers expressed as a percentage.

    :param value1: The first number to be evaluated.
    :param value1: float | int

    :param value2: The second number to be evaluated.
    :param value2: float | int

    :param absolute: Indicates the absolute value of the difference should be returned. Otherwise, the result may be a
                     negative float or integer.
    :param absolute: bool

    :param precision: The rounding precision of the resulting float.
    :type precision: int

    :rtype: float

    The formula applied is:

    .. code-block:: text

        (
            value1 - value2
            _______
            (value1 + value2) / 2
        ) * 100

    """
    if value1 == value2:
        return 0.0

    a = value1 - value2
    b = (value1 + value2) / 2

    # This should only happen when the two values are equal which is handled above.
    # if int(b) == 0:
    #     return 0.0

    result = (a / b) * 100
    if absolute:
        return round(abs(result), precision)

    return round(result, precision)


def factors_of(number):
    """Get the factors of a given number.

    :param number: The number for which the factors will be obtained.
    :type number: int

    :rtype: list[int]
    :raise: TypeError

    """
    if type(number) is not int:
        raise TypeError("Factors may only be acquired for an integer.")

    a = list()
    for i in range(1, number + 1):
        if number % i == 0:
           a.append(i)

    return a


def is_prime(number):
    """Determine whether the given number is a prime.

    :param number: The number to be checked.
    :type number: int

    :rtype: bool

    """
    try:
        return len(factors_of(number)) == 2
    except TypeError:
        return False


def median(values):
    """Get the median of the provided values.

    :param values: An iterable of values to be evaluated. They may be of different number types.

    .. note::
        This is just a convenience wrapper around the statistics module, but captures ``StatisticsError`` and returns
        ``None`` if ``values`` is empty.

    """
    try:
        return statistics.median(values)
    except statistics.StatisticsError:
        return None


def percentage(portion, total):
    """Calculate the percentage that a portion makes up of a total.

    :param portion: The portion of the total to be calculated as a percentage.
    :type portion: float | int

    :param total: The total amount.
    :type total: float | int

    :rtype: float

    .. code-block:: python

        from commonkit.utils import percentage

        p = percentage(50, 100)
        print(p + "%")

    """
    try:
        return 100.0 * portion / total
    except (TypeError, ZeroDivisionError):
        return 0.0


def product(values, base=1):
    """Get the product of the given values.

    :param values: An iterable of values to be multiplied.

    :param base: Applied to the beginning of the calculation.
    :type base: int

    """
    return reduce(operator.mul, values, base)
