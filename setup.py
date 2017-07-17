import unittest
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


packages = ['citytime']


setup(
    name="CityTime",
    version="1.1.3",
    description="A tool for comparing time between different locations/timezones",
    long_description=long_description,
    author="Thorsten Weyter",
    author_email="tweyter@gmail.com",
    license="MIT",
    url="https://github.com/tweyter/CityTime",
    packages=packages,
    test_suite='setup.my_test_suite',
    package_dir={'citytime': 'citytime'},
    keywords="time datetime olson timezone",
    install_requires=["pytz"],
    tests_require=['hypothesis'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities"
    ]
)
