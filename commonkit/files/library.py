# Imports

import csv
import io
import logging
import os
from shutil import copy2
from ..compat import JinjaEnvironment, JinjaLoader

logger = logging.getLogger(__name__)

# Exports

__all__ = (
    "append_file",
    "copy_file",
    "copy_tree",
    "parse_jinja_template",
    "read_csv",
    "read_file",
    "write_file",
    "File",
)

# Functions


def append_file(path, content, line_feed=True):
    """Append content to a file.

    :param path: The path to the file.
    :type path: str

    :param content: The content to be added.
    :type content: str

    :param line_feed: Automatically add a line feed before the content.
    :type line_feed: bool

    :rtype: bool

    """
    if not os.path.exists(path):
        return False

    _content = read_file(path)
    if line_feed:
        _content += "\n%s" % content

    write_file(path, _content)

    return True


def copy_file(from_path, to_path, make_directories=False):
    """Copy a file from one location to another.

    :param from_path: The source path.
    :type from_path: str || unicode

    :param to_path: The destination path.
    :type to_path: str || unicode

    :param make_directories: Create directories as needed along the ``to_path``.
    :type make_directories: bool

    :rtype: tuple(bool, str)
    :returns: Success or failure and a message if failure.

    .. code-block:: python

        from superpython.utils import copy_file

        copy_file("readme-template.txt", "path/to/project/readme.txt")

    """
    if make_directories:
        base_path = os.path.dirname(to_path)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    try:
        copy2(from_path, to_path)
        return True, None
    except IOError as e:
        return False, str(e)


def copy_tree(from_path, to_path):
    """Recursively copy a source directory to a given destination.

    :param from_path: The source directory.
    :type from_path: str

    :param to_path: The destination directory. This must already exist.
    :type to_path: str

    :rtype: bool
    :returns: ``True`` if successful.

    .. note::
        Errors are logged using the Python logger.

    .. code-block:: python

        from superpython.utils import copy_tree

        success = copy_tree("from/path", "to/path")
        print(success)

    """
    # Deal with absolutes and user expansion.
    source = os.path.abspath(os.path.expanduser(from_path))
    destination = os.path.abspath(os.path.expanduser(to_path))

    if not os.path.exists(destination):
        logger.error("Destination does not exist: %s" % destination)
        return False

    # Iterate through the source.
    success = True
    for root, dirs, files in os.walk(source):
        directory_path = os.path.join(destination, os.path.relpath(root, source))
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        for f in files:
            source_file = os.path.join(root, f)
            file_path = os.path.join(directory_path, f)

            try:
                copy2(source_file, file_path)
            except IOError as e:
                success = False
                logger.warning("Could not copy %s: %s" % (source_file, e))

    return success


def parse_jinja_template(path, context):
    """Parse a Jinja 2 template.

    :param path: Path to the template.
    :type path: str

    :param context: The context to be parsed into the template.
    :type context: dict

    :rtype: str

    .. code-block:: python

        from superpython.utils import parse_jinja_template

        context = {
            'domain_name': "example.com",
            'first_name': "Bob",
        }

        template = "path/to/welcome.html"

        output = parse_jinja_template(template, context)

    """
    search_path = os.path.dirname(path)
    env = JinjaEnvironment(loader=JinjaLoader(search_path))

    template_name = os.path.basename(path)
    template = env.get_template(template_name)

    return template.render(**context)


def read_csv(path, encoding="utf-8", first_row_field_names=False, **kwargs):
    """Read the contents of a CSV file.

    :param path: The path to the file.
    :type path: str

    :param encoding: The encoding of the file.
    :type encoding: str

    :param first_row_field_names: Indicates the first row contains the field names. In this case the returned rows will
                                  be a dictionary rather than a list.

    :type first_row_field_names: bool

    :rtype: list[list] || list[dict]

    kwargs are passed to Python's ``csv.DictReader`` (when ``first_row_field_names`` is ``True``) or ``csv.reader``.

    .. code-block:: text

        menu,identifier,sort_order,text,url
        main,product,10,Product,/product/
        main,solutions,20,Solutions,/solutions/
        main,resources,30,Resources,/resources/
        main,support,40,Support,https://support.example.com
        main,about,50,About,/about/
        main,contact,60,Contact,/contact/

    .. code-block:: python

        from superpython.utils import read_csv

        rows = read_csv("path/to/menus.csv", first_row_fields_names=True)
        for r in rows:
            print("%s: %s" % (row['identifier'], row['url']

    """
    with io.open(path, "r", encoding=encoding) as f:
        if first_row_field_names:
            reader = csv.DictReader(f, **kwargs)
        else:
            reader = csv.reader(f, **kwargs)

        rows = list()
        for row in reader:
            rows.append(row)

        f.close()

        return rows


def read_file(path):
    """Read a file and return its contents.

    :param path: The path to the file.
    :type path: str || unicode

    :rtype: str

    .. code-block:: python

        from superpython.utils import read_file

        output = read_file("path/to/readme.txt")
        print(output)

    """
    with io.open(path, "r", encoding="utf-8") as f:
        output = f.read()
        f.close()

        return output


def write_file(path, content="", make_directories=False):
    """Write a file.

    :param path: The path to the file.
    :type path: str || unicode

    :param content: The content of the file. An empty string is effectively the same as a "touch".
    :type content: str || unicode

    :param make_directories: Create directories as needed along the file path.
    :type make_directories: bool

    .. code-block:: python

        from superpython.utils import write_file

        write_file("path/to/readme.txt", "This is a test.")

    """
    if make_directories:
        base_path = os.path.dirname(path)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
        f.close()


# Classes


class File(object):
    """A simple helper class for working with file names.

    For more robust handling of paths, see `pathlib`_.

    .. _pathlib: https://docs.python.org/3/library/pathlib.html

    """

    def __init__(self, path):
        """Initialize the file instance.

        :param path: The path to the file.
        :type path: str

        """
        self.basename = os.path.basename(path)
        self.directory = os.path.dirname(path)
        self.extension = os.path.splitext(path)[-1]
        self.name = os.path.basename(os.path.splitext(path)[0])
        self.path = path

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.basename)

    @property
    def exists(self):
        """Indicates the file exists.

        :rtype: bool

        """
        return os.path.exists(self.path)
