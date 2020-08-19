"""
Abstract
--------

A *watcher* observes a directory or file waiting for changes to occur. This is useful for triggering other events based
on changes to the file system.

Usage
-----

Watching a Directory
....................

This example demonstrates how to watch a directory for changes to files with specific extensions.

.. code-block:: python

    from commonkit.watchers import Watcher
    import time

    directory_watcher = Watcher("path/to/watched", extensions=[".yml", ".xml"]

    print("I'm now watching %s" % directory_watcher.path)
    while True:
        try:
            updated = next(directory_watcher.watch())
            if updated:
                print("Update detected. I'm on it.")
        except KeyboardInterrupt:
            print("I quit.")
            break
        except Exception as e:
            print("I can't go on: %s" % e)
            break
        finally:
            time.sleep(5)

Watching a File
...............

This example demonstrates how to watch a specific file.

.. code-block:: python

    from commonkit.watchers import Watcher
    import time

    file_watcher = Watcher("path/to/settings.cfg")

    print("I'm now watching %s" % file_watcher.path)
    while True:
        try:
            updated = next(file_watcher.watch())
            if updated:
                print("Update detected. I'm on it.")
        except KeyboardInterrupt:
            print("I quit.")
            break
        except Exception as e:
            print("I can't go on: %s" % e)
            break
        finally:
            time.sleep(5)

Using Multiple Watchers
.......................

This example demonstrations how to enable multiple watchers at once.

.. code-block:: python

    from commonkit.watchers import Watcher
    import time

    watchers = {
        'directory': Watcher("path/to/watched", extensions=[".yml", ".xml"]),
        'settings': Watcher("path/to/settings.cfg"),
    }

    while True:
        try:
            updated = {k: next(v.watch()) for k, v in watchers.items()}
            if any(updated.values()):
                print("Update detected. I'm on it.")
        except KeyboardInterrupt:
            print("I quit.")
            break
        except Exception as e:
            print("I can't go on: %s" % e)
            break
        finally:
            time.sleep(5)

"""

from .library import Watcher

__all__ = (
    "Watcher",
)

__version__ = "0.1.0-d"
