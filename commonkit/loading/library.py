import copy
import os
from importlib import import_module
from importlib.util import find_spec

# Exports

__all__ = (
    "autodiscover",
    "find_packages",
    "has_callable",
    "import_member",
    "submodule_exists",
    "Module",
)

# Functions


def autodiscover(locations, module_name):
    """Auto discover modules of a specific name among possible locations.

    :param locations: A list of dotted path locations where the module may exist.
    :type locations: list[str]

    :param module_name: The name of the module to find.
    :type module_name: str

    """
    for dotted_path in locations:
        path = dotted_path.replace(".", os.sep)
        packages = find_packages(path)

        for package in packages:
            _dotted_path = "%s.%s" % (package, module_name)
            try:
                import_module(_dotted_path)
            except Exception:  # pragma: no cover
                # This IS tested in unit tests but for some reason does not appear in coverage.
                if submodule_exists(_dotted_path, module_name):
                    raise


def find_packages(path):
    """Get a list of Python packages on the given path.

    :param path: The path to which packages are located.
    :type path: str

    :rtype: list[str]
    :returns: A list of dotted paths for packages found at the top level of ``path``.

    """
    a = list()
    for d in os.listdir(path):
        _path = os.path.join(path, d)
        if not os.path.isdir(_path):
            continue

        if os.path.isfile(os.path.join(_path, "__init__.py")):
            dotted = path.replace(os.sep, ".") + "." + d
            a.append(dotted)

    return a


def has_callable(instance, name):
    """Indicates whether a given instance has the named callable.

    :param instance: The instance to be checked.

    :param name: The name to be confirmed as a callable.
    :type name: str

    :rtype: bool

    """
    if not hasattr(instance, name):
        return False

    method = getattr(instance, name)
    return callable(method)


def import_member(dotted_path, raise_exception=True):
    """Import the member (attribute, class or function) found at the end of a dotted path.

    :param dotted_path: The dotted path to the member.
    :type dotted_path: str

    :param raise_exception: Indicates an exception should be raised on failure.
    :type raise_exception: bool

    :returns: The member or ``None`` if it could not be imported and ``raise_exception`` is ``False``.

    :raise: ImportError
    :raises: ``ImportError`` if the member could not be imported and ``raise_exception`` is ``True``.

    """
    # Separate the module portion from the member.
    try:
        _dotted_path, member_name = dotted_path.rsplit(".", 1)
    except ValueError as e:
        if raise_exception:
            raise ImportError("Invalid dotted path: %s" % dotted_path) from e

        return None

    # Load the module.
    module = import_module(_dotted_path)

    # Attempt to acquire the member from the module.
    try:
        return getattr(module, member_name)
    except AttributeError as e:
        if raise_exception:
            raise ImportError("%s does not exist in module: %s" % (member_name, _dotted_path)) from e

        return None


def submodule_exists(package, module_name):
    """Determine whether a submodule exists within a package.

    :param package: The imported package or the dotted path as a string.
    :type package: module | str

    :param module_name: The name of the module for which to test.
    :type module_name: str

    :rtype: bool

    """
    if type(package) is str:
        try:
            package = import_module(package)
        except ImportError:
            return False

    try:
        package_name = package.__name__
        package_path = package.__path__
    except AttributeError:
        return False

    dotted_path = "%s.%s" % (package_name, module_name)
    return find_spec(dotted_path, package_path) is not None

    # From Django: When module_name is an invalid dotted path, Python raises
    # ModuleNotFoundError. AttributeError is raised on PY36 (fixed in PY37)
    # if the penultimate part of the path is not a package.
    # try:
    #     return find_spec(dotted_path, package_path) is not None
    # except (AttributeError, ModuleNotFoundError):
    #     return False

# Classes


class Module(object):
    """Encapsulates a Python module for loading."""

    def __init__(self, dotted):
        """Initialize a module instance.

        :param dotted: The dotted path to the module.
        :type dotted: str

        """
        self.dotted = dotted
        self.is_loaded = False
        self.level = len(dotted.split(".")) - 1
        self.name = dotted.split(".")[-1]
        self.path = os.path.join(*dotted.split("."))
        self._attributes = dict()
        self._module = None

    def __getattr__(self, item):
        return self._attributes.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.dotted)

    @property
    def exists(self):
        """Indicates whether the module exists.

        :rtype: bool

        """
        return find_spec(self.dotted) is not None

    def load(self):
        """Load the module.

        :rtype: bool

        """
        try:
            self._module = import_module(self.dotted)
        except ImportError:
            return False

        self._attributes['author'] = None
        try:
            # noinspection PyUnresolvedReferences
            self._attributes['author'] = self._module.__author__
        except AttributeError:
            pass

        self._attributes['docstring'] = self._module.__doc__
        # try:
        #     self._attributes['docstring'] = self._module.__doc__
        # except AttributeError:
        #     pass

        self._attributes['maintainer'] = None
        try:
            # noinspection PyUnresolvedReferences
            self._attributes['maintainer'] = self._module.__maintainer__
        except AttributeError:
            pass

        self.path = self._module.__path__

        self._attributes['version'] = None
        try:
            # noinspection PyUnresolvedReferences
            self._attributes['version'] = self._module.__version__
        except AttributeError:
            pass

        self._load()

        self.is_loaded = True

        return True

    def _load(self):
        """A hook for customizing the load. Called at the end of ``load()``."""
        pass
