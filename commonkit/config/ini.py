from configparser import ConfigParser, DuplicateOptionError, DuplicateSectionError, InterpolationMissingOptionError, \
    MissingSectionHeaderError, ParsingError
from ..files import parse_jinja_template, read_file
from .base import Base

# Classes


class INIConfig(Base):

    def __init__(self, path, auto_section=False, context=None, dummy=None, flatten=None):
        """Initialize an INI configuration.

        :param path: The path to the configuration file.
        :type path: str

        :param auto_section: Create sections dynamically if they do not exist. This prevents ``NoneType`` errors in code
                             that utilizes the config, but may be hard to troubleshoot. Use with caution.
        :type auto_section: bool

        :param context: Context is used to parse the file as a Jinja template.
        :type context: dict

        :param dummy: The name of a dummy section to create for items that exist at the beginning of the file but do not
                      fall under a section.
        :type dummy: str

        :param flatten: A section name whose items are to be accessible on the instance without referring to the section
                        name.
        :type flatten: str

        """
        super().__init__(path)

        self._auto_section = auto_section
        self._context = context
        self._dummy = dummy
        self._flatten = flatten
        self._sections = dict()

    def __getattr__(self, item):
        """Get the named section instance."""
        if self._flatten is not None and self._flatten in self._sections:
            if self._sections[self._flatten].has(item):
                return self._sections[self._flatten].get(item)

        if item not in self._sections and self._auto_section:
            return Section(item)

        return self._sections.get(item)

    def __iter__(self):
        return iter(self._sections.values())

    def __len__(self):
        return len(self._sections)

    def get(self, name, default=None, key=None):
        """Get the named value.

        :param name: The section name.
        :type name: str

        :param default: The default if the key does not exist or has no value.

        :param key: The key of the section to return.
        :type key: str

        """
        if name not in self._sections:
            return None

        section = self._sections[name]

        if key is not None:
            return section.get(key, default=default)

        return section

    def has(self, name, key=None):
        """Indicates whether the named section has been defined.

        :param name: The section name.
        :type name: str

        :param key: Also check if the key exists (and has a value other than ``None``).
        :type key: str

        :rtype: bool

        """
        if name not in self._sections:
            return False

        if key is not None:
            return self._sections[name].has(key)

        return True

    def load(self):
        """Load the configuration file.

        :rtype: bool

        """
        if not self.exists:
            return False

        ini = ConfigParser()

        if self._context is not None:
            content = parse_jinja_template(self._path, self._context)
        else:
            content = read_file(self._path)

        if self._dummy is not None:
            prepend = "[%s]\n" % self._dummy
            content = prepend + content

        possible_errors = (DuplicateOptionError, DuplicateSectionError, InterpolationMissingOptionError,
                           MissingSectionHeaderError, ParsingError)
        try:
            ini.read_string(content)
        except possible_errors as e:
            self._error = e
            return False

        for section in ini.sections():
            kwargs = dict()
            for key, value in ini.items(section):
                _key, _value = self._process_key_value_pair(key, value, section=section)
                kwargs[_key] = _value

            _section = Section(section, **kwargs)
            self._sections[section] = _section

        self.is_loaded = True

        return True


class Section(object):
    """An object-oriented representation of a configuration section from an INI file. See :py:class:`INIConfig`."""

    def __init__(self, section_name, **kwargs):
        """Initialize the section.

        :param section_name: The section name.
        :type section_name: str

        Keyword arguments are added as context variables.

        """
        self._name = section_name
        self._attributes = kwargs

    def __getattr__(self, item):
        return self._attributes.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self._name)

    def get(self, name, default=None):
        """Get the named value.

        :param name: The name of the value to return.
        :type name: str

        :param default: The default if the name does not exist or has no value.

        """
        return self._attributes.get(name, default)

    def get_attributes(self):
        """Get the section attributes.

        :rtype: dict

        """
        return self._attributes

    def get_name(self):
        """Get the section name.

        :rtype: str

        """
        return self._name

    def has(self, name):
        """Indicates whether the named variable has been defined *and* is not ``None``.

        :rtype: bool

        """
        if name in self._attributes:
            return self._attributes[name] is not None

        return False
