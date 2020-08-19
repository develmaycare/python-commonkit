import os
import shutil
from commonkit.watchers import Watcher
import time

OUTPUT_PATH = os.path.join("tests", "watched")

# Tests


class TestWatch(object):

    def test_exists(self):
        """Check that a watcher correctly identifies its existence."""
        watcher = Watcher(OUTPUT_PATH)
        assert watcher.exists is True

        nonexistent_path = os.path.join(OUTPUT_PATH, "nonexistent.txt")
        watcher = Watcher(nonexistent_path)
        assert watcher.exists is False

    def test_is_directory(self):
        """Check that a watcher correctly identifies as a directory."""
        watcher = Watcher(OUTPUT_PATH)
        assert watcher.is_directory is True
        assert watcher.is_file is False

        example_path = os.path.join("tests", "watched", "readme.txt")
        watcher = Watcher(example_path)
        assert watcher.is_directory is False
        assert watcher.is_file is True

    def test_watch(self):

        # This watcher has an invalid path.
        watcher = Watcher(os.path.join("path", "to", "nonexistent"))
        try:
            next(watcher.watch())
        except ValueError:
            assert True

        # Watcher for the directory.
        directory_watcher = Watcher(OUTPUT_PATH)

        # Watcher for a specific file.
        file_path = os.path.join(OUTPUT_PATH, "readme.txt")
        file_watcher = Watcher(file_path)

        # First pass returns True.
        assert next(directory_watcher.watch()) is True
        assert next(file_watcher.watch()) is True

        # The next pass should return False because nothing's been modified.
        assert next(directory_watcher.watch()) is False
        assert next(file_watcher.watch()) is False

        # Update time to detect modification.
        t = time.time()
        os.utime(file_path, (t, t))

        assert next(directory_watcher.watch()) is True
        assert next(file_watcher.watch()) is True

        # A bad file produces an OSError and returns None.
        bad_file_watcher = Watcher("path/to/nonexistent.txt")
        bad_file_watcher._is_file = True
        assert next(bad_file_watcher.watch()) is None

        # The two nonexistent files (symlinks to nowhere) will result in a yield of None, even when .md extension is
        # included. This helps force an OSError.
        specific_watcher = Watcher(OUTPUT_PATH, extensions=[".md"])
        assert next(specific_watcher.watch()) is None

        # Check functionality against an initially empty path with added files and extension filtering.
        empty_path = os.path.join(OUTPUT_PATH, "empty")

        os.mkdir(empty_path)

        # An empty directory should return None.
        empty_watcher = Watcher(empty_path)
        assert next(empty_watcher.watch()) is None

        # Create a file that isn't watched.
        from_path = os.path.join(OUTPUT_PATH, "readme.txt")
        to_path = os.path.join(empty_path, "readme.txt")
        shutil.copy(from_path, to_path)

        # .txt extension should return None.
        specific_watcher = Watcher(empty_path, extensions=[".md"])
        assert next(specific_watcher.watch()) is None

        # No create a file that is watched.
        to_path = os.path.join(empty_path, "readme.md")
        shutil.copy(from_path, to_path)
        assert next(specific_watcher.watch()) is True

        # Remove the empty_path to reset for the future.
        shutil.rmtree(empty_path, ignore_errors=True)
