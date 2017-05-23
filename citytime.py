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

__add__():
    Returns a new CityTime object with the daylight savings time adjusted sum of this CityTime object
    and a given timedelta.

    This method mirrors the __add__ method of datetime.datetime, except that it adjusts for daylight
    savings time. Instead of straight addition, however, this method increments the time forward or
    backward depending on the given timedelta. Forward if the timedelta is positive, backward if the
    timedelta is negative.  It will raise AmbiguousTimeError or NonExistentTimeError if the sum results
    in an ambiguous time or a non existent time (caused by the transition to/from daylight
    savings time.

__sub__():
    Returns a new CityTime object with the result of this CityTime object decremented by
    the amount of time in the given timedelta.

    This mirrors the __sub__ method of datetime.datetime, except that it adjusts for daylight
    savings time. It will raise AmbiguousTimeError or NonExistentTimeError if the product results
    in an ambiguous time or a non existent time (caused by the transition to/from daylight
    savings time.

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

        @type time: str or datetime.datetime or CityTime
        @type tz: str
        @raise TypeError:
        """
        self._is_set = False
        if time and isinstance(time, CityTime):
            self._tz = time.tzinfo()
            self._datetime = time.utc()
            self._t_zone = time.timezone()
            self._is_set = True
        elif isinstance(time, datetime.datetime) and isinstance(tz, str):
            self.set(time, tz)
        elif isinstance(time, str) and isinstance(tz, str):
            self.set_iso_format(time, tz)
        elif time is None:
            self._datetime = datetime.datetime.min
            self._t_zone = str()
            self._tz = pytz.timezone('utc')
        else:
            raise TypeError("Argument 'time' must be of type 'CityTime' or 'datetime.datetime'")

    def __str__(self):
        """
        Returns the local time in string format.

        @rtype: str
        """
        if self._datetime != datetime.datetime.min:
            return str(';'.join([self._datetime.isoformat(), self.timezone()]))
        else:
            return "CityTime object not set yet."

    def __repr__(self):
        """
        Returns the local time in string format.

        @rtype: str
        """
        if self._datetime != datetime.datetime.min:
            no_offset = self._datetime.isoformat().split(sep='+')[0]
            _repr = 'CityTime("{}", "{}")'.format(
                no_offset,
                self._tz
            )
            return _repr
        else:
            return "CityTime object not set yet."

    def __bool__(self):
        """
        Returns True if the CityTime object has been set with a local time, otherwise returns false.

        @rtype: bool
        """
        return self._is_set

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
        other_utc = getattr(other, 'utc', None)
        if other_utc and self._datetime == other_utc():
            return True
        else:
            return self._datetime == other

    def __ne__(self, other):
        """
        Returns true if this object's set time in UTC is not equal to another CityTime object's UTC time.

        For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
        object that is set to 4pm in New York on the same date, it will show as not equal, because when
        it is 4pm in Chicago it is 5pm in New York.

        @type other: CityTime
        @rtype: bool
        """
        other_utc = getattr(other, 'utc', None)
        if other_utc and self.utc() != other_utc():
            return True
        else:
            return self.utc() != other

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
        other_utc = getattr(other, 'utc', None)
        if other_utc and self.utc() < other_utc():
            return True
        else:
            return self.utc() < other

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
        if self._is_set is False:
            raise ValueError('Date/Time zone has not been set.')
        other_utc = getattr(other, 'utc', None)
        if other_utc and self._datetime <= other_utc():
            return True
        else:
            return self._datetime <= other

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
        other_utc = getattr(other, 'utc', None)
        if other_utc and self.utc() > other_utc():
            return True
        else:
            return self.utc() > other

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
        other_utc = getattr(other, 'utc', None)
        if other_utc and self.utc() >= other_utc():
            return True
        else:
            return self.utc() >= other

    def __add__(self, other):
        """
        Returns a new CityTime object with the daylight savings time adjusted sum of this CityTime object
        and a given timedelta.

        This method mirrors the __add__ method of datetime.datetime, except that it adjusts for daylight
        savings time. Instead of straight addition, however, this method increments the time forward or
        backward depending on the given timedelta. Forward if the timedelta is positive, backward if the
        timedelta is negative.  It will raise AmbiguousTimeError or NonExistentTimeError if the sum results
        in an ambiguous time or a non existent time (caused by the transition to/from daylight
        savings time.

        @type other datetime.timedelta
        @rtype: CityTime
        """
        new_object = CityTime()
        new_object.set(self.local(), self.timezone())
        new_object.increment(seconds=other.total_seconds())
        return new_object

    def __sub__(self, other):
        """
        Returns a new CityTime object with the result of this CityTime object decremented by
        the amount of time in the given timedelta.

        This mirrors the __sub__ method of datetime.datetime, except that it adjusts for daylight
        savings time. It will raise AmbiguousTimeError or NonExistentTimeError if the product results
        in an ambiguous time or a non existent time (caused by the transition to/from daylight
        savings time.

        @type other CityTime, datetime
        @rtype: CityTime
        """
        if isinstance(other, datetime.timedelta):
            new_object = CityTime()
            new_object.set(self.local(), self.timezone())
            new_object.increment(seconds=-other.total_seconds())
            return new_object
        elif isinstance(other, CityTime):
            return self.utc() - other.utc()
        elif isinstance(other, datetime.datetime):
            raise UnknownTimeZoneError("Can't subtract regular datetime from CityTime object due to lack of"
                                       " Olson timezone database information.")
        else:
            raise TypeError("Can't subtract type %s from CityTime object" % type(other))

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
        try:
            time_zone.upper()
        except AttributeError:
            raise UnknownTimeZoneError("Attribute 'time_zone' must be of type 'str'")

        try:
            tz = pytz.timezone(time_zone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise UnknownTimeZoneError(time_zone)

        if getattr(date_time, 'tzinfo', None) == pytz.timezone('UTC'):
            self._datetime = date_time
        else:
            try:
                dt = tz.localize(date_time.replace(tzinfo=None), is_dst=None)
            except AttributeError:
                raise AttributeError("Attribute 'date_time' should be of type 'datetime.datetime")
            except TypeError:
                raise TypeError("Attribute 'date_time' should be of type 'datetime.datetime")
            except NonExistentTimeError:
                raise NonExistentTimeError('That time does not exist due to the change in DST')
            except AmbiguousTimeError:
                raise AmbiguousTimeError('That time is undefined due to the change in DST')
            self._datetime = dt.astimezone(pytz.utc)

        self._t_zone = time_zone
        self._tz = tz
        self._is_set = True

    def set_iso_format(self, date_time, time_zone):
        """
        This method is called when setting the CityTime object using an ISO 8601 format
        string.
        
        ***
        The ISO formatted time MUST be UTC. It cannot accept an offset.
        ***
        
        In order to avoid having to use another dependency, it is very simple in
        its ability to parse the ISO format string. The string must be in the
        following format:
        YYYY-MM-DDTHH:MM:SS
        It will strip out and disregard any microseconds

        @type date_time: str
        @type time_zone: str
        """
        try:
            time_zone.upper()
        except AttributeError:
            raise UnknownTimeZoneError("Attribute 'time_zone' must be of type 'str'")

        try:
            tz = pytz.timezone(time_zone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise UnknownTimeZoneError(time_zone)

        try:
            no_offset = date_time.split(sep='+')
        except (AttributeError, TypeError):
            raise AttributeError('ISO Format string must be a string in the following'
                                 'format: YYYY-MM-DDTHH:MM:SS')

        if len(no_offset) > 1 and no_offset[1] != '00:00':
            raise ValueError('The ISO formatted time MUST be UTC. It cannot accept an offset.')

        split_time = no_offset[0].split(sep='.')
        form = '%Y-%m-%dT%H:%M:%S'
        utc_time = datetime.datetime.strptime(split_time[0], form)

        if len(split_time) == 2:
            dt = utc_time.replace(microsecond=int(split_time[1]), tzinfo=pytz.utc)
        else:
            dt = utc_time.replace(tzinfo=pytz.utc)

        self._datetime = dt.astimezone(pytz.utc)
        self._t_zone = time_zone
        self._tz = tz
        self._is_set = True

    def is_set(self):
        """
        Checks to see whether a CityTime object has been created with or without
        the local time being set.

        This is for instances where a someone might want to create a CityTime object, but
        will actually set its time later in the program.
        """
        if self._datetime == datetime.datetime.min:
            return False

        if self._t_zone == '':
            return False

        return True

    def check_set(self):
        if not self._is_set:
            raise ValueError('Date/Time zone has not been set.')
        return True

    def utc(self):
        """
        Outputs the time as a datetime.datetime object converted to UTC.

        @rtype : datetime.datetime
        """
        if self._is_set is True:
            return self._datetime
        else:
            raise ValueError('Date/Time zone has not been set.')

    def local(self):
        """
        Outputs the time as a datetime.datetime object with the local time zone.

        @rtype : datetime.datetime
        """
        if self._is_set is False:
            raise ValueError()

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
        if self._is_set is False:
            raise ValueError()
        dt = self._datetime
        tz = pytz.timezone(time_zone)
        return dt.astimezone(tz)

    def local_minute(self):
        """
        Get just the local time, no date info, in the form of minutes.

        @rtype : int
        """
        if self._is_set is False:
            raise ValueError()
        dt = self._datetime
        lt = dt.astimezone(self._tz)
        minutes = lt.hour * 60 + lt.minute
        return minutes

    def timezone(self):
        """
        Outputs the local time zone (Olson database, string format).

        @rtype : str
        """
        if self._is_set is False:
            raise ValueError()
        return self._t_zone

    def tzinfo(self):
        """
        Return a datetime.tzinfo implementation for the given timezone.

        Equivalent to pytz.timezone('Time_zone_string'). It can then be used with datetime,
        with pytz.localize, etc.

        @rtype : timezone
        """
        if self._is_set is False:
            raise ValueError()
        return self._tz

    def weekday(self):
        """
        Get the numerical day of the week (0 = Monday, 6 = Sunday) for the local time zone.

        @rtype: int
        """
        if self._is_set is False:
            raise ValueError()
        dt = self._datetime
        local = dt.astimezone(self._tz)

        return local.weekday()

    def day_name(self):
        """
        Get the calendar day of the week for the local time zone.

        @rtype: str
        """
        if self._is_set is False:
            raise ValueError()
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

        if self._is_set is False:
            raise ValueError()
        dt = self._datetime
        local = dt.astimezone(self._tz)
        abbr = weekdays[local.weekday()]

        return abbr

    def time_string(self):
        """
        Get the local time in HHMM format.

        @rtype: str
        """
        if self._is_set is False:
            raise ValueError()
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

        if self._is_set is False:
            raise ValueError()

        if days is None and hours is None and minutes is None and seconds is None:
            raise ValueError('Parameters missing.')
        if not all(isinstance(x, (int, float)) for x in [days, hours, minutes, seconds] if x is not None):
            raise TypeError('Increment parameters must be of type <int> or <float>')
        increment = datetime.timedelta()
        if days:
            increment += datetime.timedelta(days=days)
        if hours:
            increment += datetime.timedelta(seconds=hours * 3600)
        if minutes:
            increment += datetime.timedelta(seconds=minutes * 60)
        if seconds:
            increment += datetime.timedelta(seconds=seconds)
        result = self._datetime + increment
        assert isinstance(result, datetime.datetime)
        self._tz.normalize(result.astimezone(self._tz))
        self._datetime = result

    def local_strftime(self, form):
        """
        The equivalent of datetime.datetime.strftime.

        Convert the local time to a string as specified by the format argument. The format argument
        must be a string.

        @type form: str  # format argument
        @rtype: str
        """
        local_datetime = self.local()
        result = local_datetime.strftime(form)
        return result

    def utc_strftime(self, form):
        """
        The equivalent of datetime.datetime.strftime, but for UTC time.

        Convert the time in UTC format to a string as specified by the format argument. The format argument
        must be a string.

        @type form: str  # format argument
        @rtype: str
        """
        utc_datetime = self.utc()
        result = utc_datetime.strftime(form)
        return result

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

    def epoch(self):
        if self._is_set is True:
            epoch_base = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('UTC'))
            return int((self.utc() - epoch_base).total_seconds())
        else:
            raise ValueError('Date/Time zone has not been set.')

    def copy(self):
        """
        Returns a copy of this CityTime instance.

        @rtype: CityTime
        """
        new_object = CityTime()
        new_object.set(self.local(), self.timezone())
        return new_object

    def offset(self):
        return self.local().strftime('%z')


class Range(object):
    """
    Range extends the usefulness of CityTime objects by creating a time range between two
    times: a start time and an end time. This time range can then be compared to other
    time ranges, tested for overlapping time ranges, sliced into a new Range from two
    overlapping Ranges, etc.

    A Range object made from two CityTime objects uses copies of the original CityTime objects,
    so that if those objects are changed in the future it won't affect the Range
    object that was created. The same is true of Range objects made using a timedelta, the
    original CityTime object is copied.
    """

    def __init__(self, time_a=None, time_b=None):
        """
        Initialize the Range object.

        A blank (unset) Range object can be created, but none of its methods can
        be used until it is set using either _create_range or _create_range_timedelta.

        @param time_a:
        @param time_b:
        @return:
        """

        self._members = set()
        self._is_set = False
        if isinstance(time_b, datetime.timedelta):
            self._create_range_timedelta(time_a, time_b)
        elif all({time_a, time_b}):
            self._create_range(time_a, time_b)
        elif time_a is None and time_b is None:
            return
        else:
            raise ValueError(
                'Range object requires two parameters, either <CityTime, CityTime> or <CityTime, datetime.timedelta>'
            )

    def __bool__(self):
        return self._is_set

    def _create_range(self, time_a, time_b):
        """
        Check to see that the input values are valid, then set self._members

        @param time_a:
        @param time_b:
        @return:
        """
        if not all({isinstance(time_a, CityTime), isinstance(time_b, CityTime)}):
            raise ValueError("Both start and end times must be CityTime objects.")
        if not all({time_a.is_set(), time_b.is_set()}):
            raise ValueError("Both start and end times must be set.")

        self._members = {time_a.copy(), time_b.copy()}
        self._delta = self.end_time() - self.start_time()
        self._is_set = True

    def _create_range_timedelta(self, time_a, delta):
        """
        Create a range using a CityTime start time and a datetime.timedelta.

        If the timedelta is a negative number, the given CityTime argument
        becomes the end time.

        @type time_a: CityTime
        @type delta: datetime.timedelta
        """
        if not isinstance(time_a, CityTime):
            raise ValueError()
        if not time_a.is_set():
            raise ValueError()
        if not isinstance(delta, datetime.timedelta):
            raise ValueError()
        end_time = time_a.copy()
        end_time.increment(seconds=delta.total_seconds())
        self._members = {time_a.copy(), end_time}
        self._delta = self.end_time() - self.start_time()
        self._is_set = True

    def _reset_delta(self):
        self._delta = self.end_time() - self.start_time()

    def check_set(self):
        """
        Indicates whether the Range object has been properly set or not.

        @return:
        """
        return self._is_set

    def start_time(self):
        """
        Return the earlier of the two Range times, no matter what order they are stored in.

        @rtype: CityTime
        """
        return min(self._members)

    def end_time(self):
        """
        Return the later of the two Range times, no matter what order they are stored in.

        @rtype: CityTime
        """
        return max(self._members)

    def delta(self):
        """
        Returns the difference (timedelta) between the end time and the start time.

        @rtype: datetime.timedelta
        """
        if not self._is_set:
            return datetime.timedelta()
        return self._delta

    def contains(self, citytime_or_range_object):
        """
        Determines if the start and end times of
        one Range object fall entirely within the start and end times of another
        Range object.

        @type citytime_or_range_object: object
        @return:
        """
        def check_set(obj):
            if not self._is_set:
                raise ValueError("Range is not set.")
            if not obj.check_set():
                raise ValueError("Object to be compared is not set.")

        if isinstance(citytime_or_range_object, Range):
            check_set(citytime_or_range_object)
            if (citytime_or_range_object.start_time() >= self.start_time()) and \
                    (citytime_or_range_object.end_time() <= self.end_time()):
                return True
            return False
        elif isinstance(citytime_or_range_object, CityTime):
            check_set(citytime_or_range_object)
            if (citytime_or_range_object >= self.start_time()) and \
                    (citytime_or_range_object <= self.end_time()):
                return True
            return False
        elif citytime_or_range_object is None:
            return False
        else:
            raise TypeError("Parameter must be CityTime type, Range type, or None")

    def overlaps(self, range_object):
        """
        Determines whether the given Range object overlaps with this Range object.

        @type range_object: Range
        @rtype: datetime.timedelta
        """
        if range_object is None:
            return False
        if not isinstance(range_object, Range):
            raise TypeError("Object to be compared must be of type 'Range'")
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not range_object.check_set():
            raise ValueError("Range object to be compared is not set.")

        if (range_object.start_time() <= self.end_time()) and\
                (range_object.end_time() >= self.start_time()):
            return True
        return False

    def overlap(self, range_object):
        """
        Determines how much of the given Range object overlaps with this Range
        object.

        @type range_object: Range
        @rtype: datetime.timedelta
        """
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not range_object.check_set():
            raise ValueError("Range object to be compared is not set.")

        # If range_object is entirely outside of this Range, return a
        # timedelta of 0.
        if self.before(range_object) or self.after(range_object):
            return datetime.timedelta()

        excluded = datetime.timedelta()
        if range_object.start_time() < self.start_time():
            excluded += self.start_time() - range_object.start_time()
        if range_object.end_time() > self.end_time():
            excluded += range_object.end_time() - self.end_time()
        return range_object.delta() - excluded

    def __eq__(self, other):
        """
        Determines if one Range object is equal to another Range object.

        Equality is determined to be True if both start_times match and
        both end_times match.
        @type other: Range
        @rtype: bool
        """
        if not isinstance(other, Range):
            return False
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.start_time() == other.start_time() and self.end_time() == other.end_time():
            return True
        return False

    def __ne__(self, other):
        """
        Determines if one Range object is not equal to another Range object.

        Range objects are not equal if either the start_times or the end_times don't match.
        @type other: Range
        @rtype: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.start_time() != other.start_time() or self.end_time() != other.end_time():
            return True
        return False

    def before(self, other):
        """
        Determines if one Range object is entirely less than another Range object.

        In other words, the end time of the Range object to be checked must be
        an earlier time than the start_time of the checking object.
        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.end_time() < other.start_time():
            return True
        return False

    def after(self, other):
        """
        Determines if one Range object is entirely greater than another Range object.

        In other words, the start time of the Range object to be checked must be
        a later time than the end_time of the checking object.
        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.start_time() > other.end_time():
            return True
        return False

    def __lt__(self, other):
        """
        Determines if one Range object's duration (delta) is less than another Range object's duration.

        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.delta() < other.delta():
            return True
        return False

    def __le__(self, other):
        """
        Determines if one Range object's duration (delta) is less than another Range object's duration.

        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.delta() <= other.delta():
            return True
        return False

    def __gt__(self, other):
        """
        Determines if one Range object's duration (delta) is greater than another Range object's duration.

        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.delta() > other.delta():
            return True
        return False

    def __ge__(self, other):
        """
        Determines if one Range object's duration (delta) is greater than another Range object's duration.

        @type other: Range
        @type: bool
        """
        if not isinstance(other, Range):
            raise TypeError("unorderable types: Range, {}".format(type(other)))
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not other.check_set():
            raise ValueError("Range object to be compared is not set.")

        if self.delta() >= other.delta():
            return True
        return False

    def __str__(self):
        return "Range: start: {} - end: {}".format(
            self.start_time().__str__(),
            self.end_time().__str__()
        )

    def __repr__(self):
        return "Range: start: {} - end: {}".format(
            self.start_time().__str__(),
            self.end_time().__str__()
        )

    def extend(self, added_delta):
        """
        Extend the range by increasing end_time by the amount of time in the
        delta argument.

        @type added_delta: datetime.timedelta
        @return:
        """
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not isinstance(added_delta, datetime.timedelta):
            raise TypeError("{} is not of type datetime.timedelta".format(repr(added_delta)))

        if added_delta < datetime.timedelta():
            raise ValueError("Extend only takes a positive timedelta value.")

        self.end_time().increment(seconds=added_delta.total_seconds())
        self._reset_delta()

    def extend_prior(self, added_delta):
        """
        Extend the range by decreasing start_time by the amount of time in the
        delta argument.

        @param added_delta:
        @return:
        """
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not isinstance(added_delta, datetime.timedelta):
            raise TypeError("{} is not of type datetime.timedelta".format(added_delta.__repr__()))

        if added_delta < datetime.timedelta():
            raise ValueError("Extend_prior only takes a positive timedelta value.")

        self.start_time().increment(seconds=-added_delta.total_seconds())
        self._reset_delta()

    def replace_start_time(self, new_start_time):
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not isinstance(new_start_time, CityTime):
            raise TypeError("{} is not of type CityTime".format(new_start_time.__repr__()))
        self._members.remove(self.start_time())
        self._members.add(new_start_time)
        self._reset_delta()

    def replace_end_time(self, new_end_time):
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not isinstance(new_end_time, CityTime):
            raise TypeError("{} is not of type CityTime".format(new_end_time.__repr__()))
        self._members.remove(self.end_time())
        self._members.add(new_end_time)
        self._reset_delta()

    def intersection(self, range_object):
        """
        Create a new range from the intersection of two ranges.

        The start time and end time are taken from where the two ranges overlap.
        @param range_object:
        @return:
        """
        if not self._is_set:
            raise ValueError("Range is not set.")
        if not range_object.check_set():
            raise ValueError("Range object to be compared is not set.")

        # If range_object is entirely outside of (greater than or less than) this
        # Range object, return None
        if self.after(range_object) or self.before(range_object):
            return None
        # If the range_object is contained entirely within this Range, just return
        # the range_object.
        if self.contains(range_object):
            return range_object
        # If this object is contained entirely within the range_object, just return
        # this object.
        if range_object.contains(self):
            return self

        if self.start_time() <= range_object.start_time() <= self.end_time():
            new_start_time = range_object.start_time()
        else:
            new_start_time = self.start_time()
        if self.start_time() <= range_object.end_time() <= self.end_time():
            new_end_time = range_object.end_time()
        else:
            new_end_time = self.end_time()
        return Range(new_start_time, new_end_time)

    def shift(self, delta):
        """
        Shift the time of the range.

        Works by incrementing start_time and end_time equally by the increment given in delta.
        @type delta: datetime.timedelta
        @return:
        """
        if not isinstance(delta, datetime.timedelta):
            raise TypeError('{} is wrong type. Must be datetime.timedelta'.format(delta))

        for time_value in self._members:
            time_value.increment(seconds=delta.total_seconds())
        self._reset_delta()

    def copy(self):
        """
        Create a copy of this Range instance.

        @rtype: Range
        """
        if not self._is_set:
            raise ValueError("Range is not set.")

        return Range(self.start_time().copy(), self.end_time().copy())

    def timedelta_to_h_mm(self):
        """

        :rtype: str
        """
        delta = self.delta()
        h, mm = divmod(int(delta.total_seconds()), 3600)
        m, _ = divmod(mm, 60)
        return '{0:01d}:{1:02d}'.format(h, m)
