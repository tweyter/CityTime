"""
The CityTime object is my solution for the headache of time zones and daylight savings time.  It takes
the local time and the local time zone, and translates the time into UTC.  The time can then be reproduced
in various formats and also incremented forward and back while still adjusting for daylight savings time.
"""

__author__ = 'Thorsten'

from calendar import day_name
import datetime
import pytz
from pytz.exceptions import AmbiguousTimeError
from pytz.exceptions import NonExistentTimeError


class CityTime(object):
    """
    Object used for handling local times at the various airports flown to.

    It translates everything to UTC, and then attaches the time zone for translating back to local time.
    CityTime can also handle incrementing the time forward or back, in order to compare two separate times
    with each other.

    """
    def __init__(self, time=None, tz=None):
        """
        CityTime objects can be instantiated using no parameters (creating a blank object that must be
        set later), a datetime.datetime object + time zone string, or another CityTime object.

        Parameter tz will be ignored if parameter time is of type CityTime.

        @type time: unknown or CityTime
        @type tz: str
        @raise TypeError:
        """
        if time and isinstance(time, CityTime):
            self._tz = time.tzinfo
            self._datetime = time.utc
            self._t_zone = time.timezone
        elif time and tz:
            self.set(time, tz)
        else:
            self._datetime = datetime.datetime.min
            self._t_zone = str()
            self._tz = pytz.timezone('utc')

    def __str__(self):
        if self._datetime != datetime.datetime.min:
            return str(self.local)
        else:
            return "CityTime object not set yet."

    def __bool__(self):
        if self._datetime == datetime.datetime.min:
            return False
        else:
            return True

    def __hash__(self):
        return self._datetime.__hash__()

    def __eq__(self, other):
        """
        Compare two CityTime objects

        if self.utc == other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return False
        if self.utc == getattr(other, 'utc'):
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Compare two CityTime objects

        if self.utc != other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return True
        if self.utc != getattr(other, 'utc'):
            return True
        else:
            return False

    def __lt__(self, other):
        """
        Compare two CityTime objects

        if self.utc < other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return NotImplemented
        if self.utc < getattr(other, 'utc'):
            return True
        else:
            return False

    def __le__(self, other):
        """
        Compare two CityTime objects

        if self.utc <= other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return NotImplemented
        if self.utc <= getattr(other, 'utc'):
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Compare two CityTime objects

        if self.utc > other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return NotImplemented
        if self.utc > getattr(other, 'utc'):
            return True
        else:
            return False

    def __ge__(self, other):
        """
        Compare two CityTime objects

        if self.utc >= other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not (isinstance(other, CityTime) and hasattr(other, 'utc')):
            return NotImplemented
        if self.utc >= getattr(other, 'utc'):
            return True
        else:
            return False

    def set(self, date_time, time_zone):

        """
        Sets the local time and then translates it to UTC.

        @type date_time: datetime.datetime
        @type time_zone: str
        """
        if isinstance(time_zone, str):
            self._t_zone = time_zone
            self._tz = pytz.timezone(time_zone)
        else:
            raise ValueError("Second argument must be of type string")

        if isinstance(date_time, datetime.datetime):
            tz = pytz.timezone(time_zone)
            dt = tz.localize(date_time.replace(tzinfo=None))
            self._datetime = dt.astimezone(pytz.utc)
        else:
            raise ValueError("First parameter must be of type datetime.datetime")

    def check_set(self):
        """
        Checks to see if self.set() has been called and instance attributes are properly set
        """
        if self._datetime == datetime.datetime.min:
            raise ValueError('Date has not been set.')

        if self._t_zone == '':
            raise ValueError('Time zone has not been set.')

    @property
    def utc(self):
        """
        Get the time in UTC.

        @rtype : datetime.datetime
        """
        self.check_set()

        return self._datetime

    @property
    def local(self):
        """
        Get the time in the local time zone.

        @rtype : datetime.datetime
        """
        self.check_set()

        dt = self._datetime
        return dt.astimezone(self._tz)

    def astimezone(self, time_zone):
        """
        Get the what the local time would be in a different time zone.

        @type time_zone: str
        @rtype: datetime.datetime
        """
        self.check_set()
        dt = self._datetime
        tz = pytz.timezone(time_zone)
        return dt.astimezone(tz)

    @property
    def local_minute(self):
        """
        Get just the local time, no date info, in the form of minutes.

        @rtype : int
        """
        self.check_set()

        dt = self._datetime
        lt = dt.astimezone(self._tz)
        minutes = lt.hour * 60 + lt.minute
        return minutes

    @property
    def timezone(self):
        """
        Find the local time zone.

        @rtype : str
        """
        self.check_set()
        return self._t_zone

    @property
    def tzinfo(self):
        """
        Get the local time zone tzinfo object.

        @rtype : timezone
        """
        self.check_set()
        return self._tz

    @property
    def weekday(self):
        """
        Get the numerical day of the week (0 = Monday, 6 = Sunday)

        @rtype: int
        """
        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)

        return local.weekday()

    @property
    def day_name(self):
        """
        Get the calendar day of the week.

        @rtype: str
        """
        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        name = day_name[local.weekday()]  # from calendar

        return name

    @property
    def day_abbr(self):
        """
        Get the abbreviated form of the calendar day of the week.

        @rtype: str
        """
        weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        abbr = weekdays[local.weekday()]

        return abbr

    @property
    def time_string(self):
        """
        Get the local time in HHMM format.

        @rtype: str
        """
        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        time_string = local.strftime('%H%M')

        return time_string

    def increment(self, days=None, hours=None, minutes=None, seconds=None):
        """
        Increment the time forward or back.  This is used in order to adjust for local time zones and
        daylight savings time.

        @type days: int
        @type hours: int
        @type minutes: int
        @type seconds: int
        """

        self.check_set()
        if not days and not hours and not minutes and not seconds:
            raise ValueError('Parameters missing.')
        dt = self._tz.normalize(self._datetime)
        increment = datetime.timedelta(seconds=0)
        if days:
            increment += datetime.timedelta(days=days)
        if hours:
            increment += datetime.timedelta(seconds=hours * 3600)
        if minutes:
            increment += datetime.timedelta(seconds=minutes * 60)
        if seconds:
            increment += datetime.timedelta(seconds=seconds)
        result = dt + increment
        assert isinstance(result, datetime.datetime)
        utc_result = result.astimezone(pytz.utc)
        # ... check to see if the local time is during the change to/from daylight savings time
        try:
            self._tz.localize(result.replace(tzinfo=None), is_dst=False)
        except AmbiguousTimeError:
            print('pytz.exceptions.AmbiguousTimeError: %s' % result)
        try:
            self._tz.localize(result.replace(tzinfo=None), is_dst=False)
        except NonExistentTimeError:
            print('pytz.exceptions.NonExistentTimeError: %s' % result)
        # ...
        self._datetime = utc_result
