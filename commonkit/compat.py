import re

HTML_REGEX = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

try:
    from bs4 import BeautifulSoup
    BEAUTIFUL_SOUP_ENABLED = True

    def remove_html(string):
        return "".join(BeautifulSoup(string, "html.parser").find_all(text=True))
except ImportError:
    BEAUTIFUL_SOUP_ENABLED = False
    BeautifulSoup = None

    def remove_html(string):
        # See https://stackoverflow.com/a/12982689/241720
        return re.sub(HTML_REGEX, "", string)

try:
    from jinja2 import Environment as JinjaEnvironment, FileSystemLoader as JinjaLoader, Template as JinjaTemplate
    JINJA_ENABLED = True
except ImportError:
    JINJA_ENABLED = False
    JinjaEnvironment = None
    JinjaTemplate = None


try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import get_formatter_by_name
    PYGMENTS_ENABLED = True
except ImportError:
    highlight = None
    get_lexer_by_name = None
    get_formatter_by_name = None
    PYGMENTS_ENABLED = False


try:
    from unidecode import unidecode
except ImportError:
    unidecode = None
