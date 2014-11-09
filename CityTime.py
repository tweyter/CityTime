"""
CityTime

Dependencies:
    pytz

Thanks:
    /u/phira

The CityTime object is my solution for the headache of time zones and daylight savings time.  It takes
the local time and the local time zone, and translates the time into UTC.  The time can then be reproduced
in various formats and also incremented forward and back while still adjusting for daylight savings time.

CityTime is a tool for comparing the time in two different cities. For example, let's say it is 5pm in New York
and 4pm in Chicago. CityTime will take both of those times and time zones, convert them to UTC, and by comparing
the two CityTime objects, will tell you if they are the same time or not (in this case, they are).

Let's say it's 8pm in Tokyo on November 1 (UTC + 9), and 7am in New York on the same date (UTC - 4). If you
create a CityTime object for each city, and compare the two, it will show that they are the same. However,
if you tried the same thing on November 3 (after Daylight Savings Time ends), they will be different,
because Japan does not follow Daylight Savings Time.

CityTime handles cases like those mentioned above by converting the input local time to UTC, while storing
the Olson Database time zone, rather than just using a UTC offset. This way, local differences in the start
and end of Daylight Savings Time are accounted for.

CityTime has the following methods:

set(datetime, time_zone):
or
set(other_CityTime_object)
    Allows setting the local time after a CityTime object has been created.
    Input can be with either another CityTime object, or with a datetime.datetime object
    plus a time zone string that refers to a time zone in the Olson database.
    It is important to note that when initiating or setting a CityTime object,
    the local time must include the date and the time zone. Otherwise, there would be no
    way to account for Daylight Savings Time.

local():
    Outputs the time as a datetime.datetime object with the local time zone.

utc():
    Outputs the time as a datetime.datetime object converted to UTC.

check_set():
    Checks to see whether a CityTime object has been created with or without
    the local time being set.

    This is for instances where a someone might want to create a CityTime object, but
    will actually set its time later in the program.

astimezone(time_zone):
    Check to see what the local time would be in a different time zone.
    Let's say it is 8pm in Tokyo on November 1, and we would like to know what time
    it is in New York. Calling .astimezone('America/New_York') from our CityTime object will
    show that it is 7am in New York.

local_minute():
    Get just the local time, no date info, in the form of minutes.

timezone():
    Outputs the local time zone (Olson database, string format).

tzinfo():
    Return a datetime.tzinfo implementation for the given timezone.

    Equivalent to pytz.timezone('Time_zone_string'). It can then be used with datetime,
    with pytz.localize, etc.

weekday()
    Get the numerical day of the week (0 = Monday, 6 = Sunday) for the local time zone.

day_name():
    Get the calendar day of the week for the local time zone.

day_abbr():
    Get the abbreviated form of the calendar day of the week for the local time zone.

time_string():
    Get the local time in HHMM format.

increment(days, hours, minutes, seconds):
    Increment the time forward or back while adjusting for daylight savings time.

    This increments the underlying UTC time, but it also checks to make sure that the
    equivalent local time is a valid time.

    For example, let's say it's 7am in New York on November 1. We want to know what the local
    time will be 24 hours later. By incrementing the time by +24 hours, it will show that the
    local time is now 6am. This is due to daylight savings time ending at 2am on November 2.

local_strftime(format):
    The equivalent of datetime.datetime.strftime.

    Convert the local time to a string as specified by the format argument. The format argument
    must be a string.

utc_strftime(format):
    The equivalent of datetime.datetime.strftime, but for UTC time.

    Convert the time in UTC format to a string as specified by the format argument. The format argument
    must be a string.

Magic Methods:
__str__():
    Returns the local time in string format.

__bool__():
    Returns True if the CityTime object has been set with a local time, otherwise returns false.

__hash__():
    Returns the hash from datetime.datetime set to UTC.

__eq__():
    Returns true if this object's set time in UTC is equal to another CityTime object's UTC time.

    For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
    object that is set to 5pm in New York on the same date, it will show as equal.

__ne__():
    Returns true if this object's set time in UTC is not equal to another CityTime object's UTC time.

    For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
    object that is set to 4pm in New York on the same date, it will show as not equal, because when
    it is 4pm in Chicago it is 5pm in New York.

__lt__():
    Returns true if this object's set time in UTC is earlier than another CityTime object's UTC time.

    For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
    object that is set to 5pm in New York on the same date, it will return True, however if the
    same comparison is made when this object is set to 4pm in Chicago, it will return False because when
    it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

__le__():
    Returns true if this object's set time in UTC is earlier than or equal to another CityTime
    object's UTC time.

    For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
    object that is set to 5pm in New York on the same date, it will return True. If the
    same comparison is made when this object is set to 4pm in Chicago, it will also return True
    because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
    this object is set to 5pm in Chicago, the comparison will then return False becaues 5pm in
    Chicago is equivalent to 6pm in New York.

__gt__():
    Returns true if this object's set time in UTC is later than another CityTime object's UTC time.

    For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
    object that is set to 5pm in New York on the same date, it will return True, however if the
    same comparison is made when this object is set to 4pm in Chicago, it will return False because when
    it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

__ge__():
    Returns true if this object's set time in UTC is later than or equal to another CityTime
    object's UTC time.

    For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
    object that is set to 5pm in New York on the same date, it will return True. If the
    same comparison is made when this object is set to 4pm in Chicago, it will also return True
    because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
    this object is set to 3pm in Chicago, the comparison will then return False becaues 3pm in
    Chicago is equivalent to 4pm in New York.


There are also three exceptions inherited from pytz:
AmbiguousTimeError:
    Handles the end of Daylight Savings Time, when the local time between 1:00am and 2:00am occurs twice.
    At 2:00am, people set their clocks back an hour to 1:00am, and the clock runs from 1:00am through
    1:59am twice.

NonExistentTimeError:
    Handles the start of Daylight Savings Time, when the local time between 1:00am and 2:00am is skipped.
    At 1:00am, people set their clocks forward an hour to 2:00am, thus the clock never runs through 1:01am
    to 1:59am.

UnknownTimeZoneError:
    Raised if the user tries to pass an unknown time zone string (One that is not in the Olson database).

"""


from calendar import day_name
import datetime
import pytz
from pytz.exceptions import AmbiguousTimeError
from pytz.exceptions import NonExistentTimeError
from pytz.exceptions import UnknownTimeZoneError


class CityTime(object):
    """
    Object used for handling local times at different cities or time zones.

    It translates everything to UTC, and then attaches the time zone for translating back to local time.
    CityTime can also handle incrementing the time forward or back, in order to compare two separate UTC
    equivalent times with each other.

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
        """
        Returns the local time in string format.

        @rtype: str
        """
        if self._datetime != datetime.datetime.min:
            return str(self.local)
        else:
            return "CityTime object not set yet."

    def __bool__(self):
        """
        Returns True if the CityTime object has been set with a local time, otherwise returns false.

        @rtype: bool
        """
        if self._datetime == datetime.datetime.min:
            return False
        else:
            return True

    def __hash__(self):
        """
        Returns the hash from datetime.datetime set to UTC.

        @rtype: int
        """
        return self._datetime.__hash__()

    def __eq__(self, other):
        """
        Returns true if this object's set time in UTC is equal to another CityTime object's UTC time.

        For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
        object that is set to 5pm in New York on the same date, it will show as equal.

        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() == other_utc():
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Returns true if this object's set time in UTC is not equal to another CityTime object's UTC time.

        For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
        object that is set to 4pm in New York on the same date, it will show as not equal, because when
        it is 4pm in Chicago it is 5pm in New York.

        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() != other_utc():
            return True
        else:
            return False

    def __lt__(self, other):
        """
        Returns true if this object's set time in UTC is earlier than another CityTime object's UTC time.

        For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
        object that is set to 5pm in New York on the same date, it will return True, however if the
        same comparison is made when this object is set to 4pm in Chicago, it will return False because when
        it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

        if self.utc < other.utc
        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() < other_utc():
            return True
        else:
            return False

    def __le__(self, other):
        """
        Returns true if this object's set time in UTC is earlier than or equal to another CityTime
        object's UTC time.

        For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
        object that is set to 5pm in New York on the same date, it will return True. If the
        same comparison is made when this object is set to 4pm in Chicago, it will also return True
        because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
        this object is set to 5pm in Chicago, the comparison will then return False becaues 5pm in
        Chicago is equivalent to 6pm in New York.

        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() <= other_utc():
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Returns true if this object's set time in UTC is later than another CityTime object's UTC time.

        For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
        object that is set to 5pm in New York on the same date, it will return True, however if the
        same comparison is made when this object is set to 4pm in Chicago, it will return False because when
        it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() > other_utc():
            return True
        else:
            return False

    def __ge__(self, other):
        """
        Returns true if this object's set time in UTC is later than or equal to another CityTime
        object's UTC time.

        For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
        object that is set to 5pm in New York on the same date, it will return True. If the
        same comparison is made when this object is set to 4pm in Chicago, it will also return True
        because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
        this object is set to 3pm in Chicago, the comparison will then return False becaues 3pm in
        Chicago is equivalent to 4pm in New York.

        @type other: CityTime
        @rtype: bool
        """
        if not isinstance(other, CityTime):
            return False
        try:
            other_utc = getattr(other, 'utc')
        except AttributeError:
            return False
        if self.utc() >= other_utc():
            return True
        else:
            return False

    def set(self, date_time, time_zone):

        """
        Allows setting the local time after a CityTime object has been created.

        Input can be with either another CityTime object, or with a datetime.datetime object
        plus a time zone string that refers to a time zone in the Olson database.
        It is important to note that when initiating or setting a CityTime object,
        the local time must include the date and the time zone. Otherwise, there would be no
        way to account for Daylight Savings Time.

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
        Checks to see whether a CityTime object has been created with or without
        the local time being set.

        This is for instances where a someone might want to create a CityTime object, but
        will actually set its time later in the program.
        """
        if self._datetime == datetime.datetime.min:
            raise ValueError('Date has not been set.')

        if self._t_zone == '':
            raise ValueError('Time zone has not been set.')

    def utc(self):
        """
        Outputs the time as a datetime.datetime object converted to UTC.

        @rtype : datetime.datetime
        """
        self.check_set()

        return self._datetime

    def local(self):
        """
        Outputs the time as a datetime.datetime object with the local time zone.

        @rtype : datetime.datetime
        """
        self.check_set()

        dt = self._datetime
        return dt.astimezone(self._tz)

    def astimezone(self, time_zone):
        """
        Check to see what the local time would be in a different time zone.

        Let's say it is 8pm in Tokyo on November 1, and we would like to know what time
        it is in New York. Calling .astimezone('America/New_York') from our CityTime object will
        show that it is 7am in New York.

        @type time_zone: str
        @rtype: datetime.datetime
        """
        self.check_set()
        dt = self._datetime
        tz = pytz.timezone(time_zone)
        return dt.astimezone(tz)

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

    def timezone(self):
        """
        Outputs the local time zone (Olson database, string format).

        @rtype : str
        """
        self.check_set()
        return self._t_zone

    def tzinfo(self):
        """
        Return a datetime.tzinfo implementation for the given timezone.

        Equivalent to pytz.timezone('Time_zone_string'). It can then be used with datetime,
        with pytz.localize, etc.

        @rtype : timezone
        """
        self.check_set()
        return self._tz

    def weekday(self):
        """
        Get the numerical day of the week (0 = Monday, 6 = Sunday) for the local time zone.

        @rtype: int
        """
        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)

        return local.weekday()

    def day_name(self):
        """
        Get the calendar day of the week for the local time zone.

        @rtype: str
        """
        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        name = day_name[local.weekday()]  # from calendar

        return name

    def day_abbr(self):
        """
        Get the abbreviated form of the calendar day of the week for the local time zone.

        @rtype: str
        """
        weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

        self.check_set()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        abbr = weekdays[local.weekday()]

        return abbr

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
        Increment the time forward or back while adjusting for daylight savings time.

        This increments the underlying UTC time, but it also checks to make sure that the
        equivalent local time is a valid time.

        For example, let's say it's 7am in New York on November 1. We want to know what the local
        time will be 24 hours later. By incrementing the time by +24 hours, it will show that the
        local time is now 6am. This is due to daylight savings time ending at 2am on November 2.

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

    def local_strftime(self, form):
        """
        The equivalent of datetime.datetime.strftime.

        Convert the local time to a string as specified by the format argument. The format argument
        must be a string.

        @type form: str  # format argument
        @rtype: str
        """
        local_datetime = self.local()
        try:
            result = local_datetime.strftime(form)
        except ValueError:
            return
        else:
            return local_datetime.strftime(form)

    def utc_strftime(self, form):
        """
        The equivalent of datetime.datetime.strftime, but for UTC time.

        Convert the time in UTC format to a string as specified by the format argument. The format argument
        must be a string.

        @type form: str  # format argument
        @rtype: str
        """
        utc_datetime = self.utc()
        try:
            result = utc_datetime.strftime(form)
        except ValueError:
            return
        else:
            return utc_datetime.strftime(form)

    @classmethod
    def today(cls):
        """
        Returns a CityTime object set to the current time in UTC.

        @rtype: CityTime
        """
        current_time = datetime.datetime.today()
        return cls(current_time, 'UTC')

    @classmethod
    def now(cls, zone):
        """
        Returns a CityTime object set to the user's current local time, but taking a user input
        time zone.

        @type zone: str
        @rtype: CityTime
        """
        if not zone:
            raise ValueError
        try:
            pytz.timezone(zone)
        except UnknownTimeZoneError:
            raise UnknownTimeZoneError(zone)
        else:
            current_time = datetime.datetime.now()
            return cls(current_time, zone)
