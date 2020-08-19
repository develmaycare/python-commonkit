from commonkit.pluggable import PluginManager


class TestPluginManager(object):
    """Testing the plugin manager is sufficient for testing related resources."""

    def test_load(self):
        enabled_plugins = [
            "tests.plugins.testing1",
            "tests.plugins.testing2",
            "tests.plugins.testing3",
            "tests.plugins.nonexistent",
        ]

        manager = PluginManager(plugins=enabled_plugins)
        count = manager.load()

        # Three plugins exist.
        count_3 = 3
        assert count == count_3

        # One plugin does not exist.
        count_1 = 1
        assert len(manager.errors) == count_1

        # Plugs will not be loaded a second time.
        count = manager.load()
        assert count == count_3

        # Iterating over the plugins should produce the same count.
        count = 0
        # noinspection PyUnusedLocal
        for plugin in manager:
            count += 1

        assert count == count_3
