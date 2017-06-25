from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="CityTime",
    version="1.1.0",
    description="Handling time comparisons",
    long_description=long_description,
    author="Thorsten Weyter",
    author_email="tweyter@gmail.com",
    license="MIT",
    url="https://github.com/tweyter/CityTime",
    keywords="time datetime olson timezone",
    install_requires=["pytz", "hypothesis", ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities"
    ]
)
