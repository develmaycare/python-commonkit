# Imports

import importlib

# Classes


class MountPoint(type):
    """The mount point establishes the base or "root" of all plugins. Any class that sets ``__metaclass__`` to
    ``MountPoint`` will automatically be "registered" as a plugin.

    Code containing plugin classes must still be loaded somehow. See :py:class:`PluginManager`.

    """

    # noinspection PyMissingConstructor,PyUnusedLocal
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "plugins"):
            # The absence of plugins means this is the mount point and not an implementation.
            cls.plugins = list()
        else:
            # Otherwise this is a plugin implementation which should be "registered" as a plugin.
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        """Get the plugins that have been registered.

        ``args`` and ``kwargs`` are passed as is to the ``__init__`` method of the plugin.

        :rtype: list

        """
        return [p(*args, **kwargs) for p in cls.plugins]


# noinspection PyCompatibility
class PluginProvider(metaclass=MountPoint):
    """Any class that extends this class will be registered as a plugin. You may also define your own class or classes
    as long as :py:class:`MountPoint` is used for ``__metaclass__``.

    """
    pass


class PluginManager(object):
    """While the mount points provide automatic registration of plugins, the code where the plugins lives must still be
    loaded in order for registration to occur.

    The plugin manager helps find and import plugins.

    .. code-block:: python

        # Plugins are given using dotted path notation.
        enabled_plugins = [
            "path.to.plugin1",
            "path.to.plugin2",
            "path.to.plugin3",
        ]

        manager = PluginManager(plugins=enabled_plugins)
        manager.load()

    """

    def __init__(self, plugins=None, provider=None):
        """Initialize the manager.

        :param plugins: A list of plugins in dotted path format.
        :type plugins: list | tuple

        """
        self.errors = list()
        self.provider = provider or PluginProvider
        self._dotted_paths = plugins or list()
        self._plugins = list()

    def __iter__(self):
        return iter(self._plugins)

    def load(self, *args, **kwargs):
        """Load the plugins given when the manager was instantiated.

        ``args`` and ``kwargs`` are passed as is to the ``__init__`` method of each plugin class that has been
        registered.

        :rtype: int
        :returns: The number of plugins loaded.

        """
        if len(self._plugins) > 0:
            return len(self._plugins)

        count = 0
        for dotted_path in self._dotted_paths:
            try:
                importlib.import_module(dotted_path)
                count += 1
            except ImportError as e:
                self.errors.append(e)

        cls = self.provider
        self._plugins = cls.get_plugins(*args, **kwargs)

        return count
