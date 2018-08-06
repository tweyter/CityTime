import codecs
import os
import re

from setuptools import setup, find_packages


NAME = "CityTime"
PACKAGES = find_packages(where='src')
META_PATH = os.path.join('src', 'citytime', '__init__.py')
KEYWORDS="time datetime olson timezone"
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Utilities",
]
INSTALL_REQUIRES = ['pytz']

SETUP_REQUIRES = ['pytest-runner']

TESTS_REQUIRE = ['pytest', 'pytest-cov', 'mypy', 'hypothesis']

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{}__ string.".format(meta))


# Get the long description from the README file
with open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


VERSION = find_meta("version")
LONG = (
    read("README.rst")
    + "\n\n"
    + '=============='
    + '\n\n'
    + read('CHANGELOG.rst')
)

if __name__ == '__main__':
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("url"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
        tests_require=TESTS_REQUIRE,
    )

