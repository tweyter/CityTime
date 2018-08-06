
from .citytime import CityTime, Range


__version__ = "1.0.0"

__title__ = "CityTime"
__description__ = "A tool for comparing time between different locations/timezones"
__url__ = "https://github.com/tweyter/CityTime"
__uri__ = __url__
__author__ = "Thorsten Weyter"
__email__ = "tweyter@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2015 Thorsten Weyter"

# As suggested by Kenneth Reitz:
# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler  # type: ignore
except ImportError:
    class NullHandler(logging.Handler):  # type: ignore
        def emit(self, record):  # type: ignore
            pass

logging.getLogger(__name__).addHandler(NullHandler())
