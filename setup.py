# See https://packaging.python.org/en/latest/distributing.html
# and https://docs.python.org/2/distutils/setupscript.html
# and https://pypi.python.org/pypi?%3Aaction=list_classifiers
from setuptools import setup, find_packages


def read_file(path):
    with open(path, "r") as f:
        contents = f.read()
        f.close()
    return str(contents)


setup(
    name='python-commonkit',
    version=read_file("VERSION.txt"),
    description=read_file("DESCRIPTION.txt"),
    long_description=read_file("README.markdown"),
    long_description_content_type="text/markdown",
    author='Shawn Davis',
    author_email='shawn@develmaycare.com',
    url="https://develmaycare.com/products/python/commonkit/",
    download_url='https://github.com/develmaycare/python-commonkit',
    project_urls={
        'Documentation': 'https://docs.develmaycare.com/en/python-commonkit/latest/',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/develmaycare/python-commonkit/',
        'Tracker': 'https://github.com/develmaycare/python-commonkit/issues/',
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    # packages=["commonkit"],
    include_package_data=True,
    install_requires=[
        "six",
    ],
    extras_require={
        'all': [
            "beautifulsoup4",
            "colorama",
            "jinja2",
            "pygments",
            "SQLAlchemy",
            "tabulate",
            "unidecode",
        ],
        'database': [
            "SQLAlchemy",
        ],
        'mssql': [
            "pyodbc",
            "SQLAlchemy",
        ],
        'oracle': [
            "cx_Oracle",
            "SQLAlchemy",
        ],
        'pgsql': [
            "psycopg2-binary",
            "SQLAlchemy",
        ],
        'shell': [
            "colorama",
            "tabulate",
        ],
        'strings': [
            "beautifulsoup4",
            "jinja2",
            "pygments",
            "unidecode",
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
    tests_require=[
        "beautifulsoup4",
        "colorama",
        "coverage",
        'cx_Oracle',
        "jinja2",
        "psycopg2-binary",
        "pyodbc",
        "pytest",
        "pygments",
        "six",
        "SQLAlchemy",
        "tablib",
        "tabulate",
        "unidecode",
    ],
    test_suite='runtests.runtests'
)
