#CityTime

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

###set(datetime, time_zone):
or
###set(other_CityTime_object):
Allows setting the local time after a CityTime object has been created.
Input can be with either another CityTime object, or with a datetime.datetime object
plus a time zone string that refers to a time zone in the Olson database.
It is important to note that when initiating or setting a CityTime object,
the local time must include the date and the time zone. Otherwise, there would be no
way to account for Daylight Savings Time.

###local():
Outputs the time as a datetime.datetime object with the local time zone.

###utc():
Outputs the time as a datetime.datetime object converted to UTC.

###check_set():
Checks to see whether a CityTime object has been created with or without
the local time being set.

This is for instances where a someone might want to create a CityTime object, but
will actually set its time later in the program.

###astimezone(time_zone):
Check to see what the local time would be in a different time zone.
Let's say it is 8pm in Tokyo on November 1, and we would like to know what time
it is in New York. Calling .astimezone('America/New_York') from our CityTime object will
show that it is 7am in New York.

###local_minute():
Get just the local time, no date info, in the form of minutes.

###timezone():
Outputs the local time zone (Olson database, string format).

###tzinfo():
Return a datetime.tzinfo implementation for the given timezone.

Equivalent to pytz.timezone('Time_zone_string'). It can then be used with datetime,
with pytz.localize, etc.

###weekday()
Get the numerical day of the week (0 = Monday, 6 = Sunday) for the local time zone.

###day_name():
Get the calendar day of the week for the local time zone.

###day_abbr():
Get the abbreviated form of the calendar day of the week for the local time zone.

###time_string():
Get the local time in HHMM format.

###increment(days, hours, minutes, seconds):
Increment the time forward or back while adjusting for daylight savings time.

This increments the underlying UTC time, but it also checks to make sure that the
equivalent local time is a valid time.

For example, let's say it's 7am in New York on November 1. We want to know what the local
time will be 24 hours later. By incrementing the time by +24 hours, it will show that the
local time is now 6am. This is due to daylight savings time ending at 2am on November 2.

###local_strftime(format):
The equivalent of datetime.datetime.strftime.

Convert the local time to a string as specified by the format argument. The format argument
must be a string.

###utc_strftime(format):
The equivalent of datetime.datetime.strftime, but for UTC time.

Convert the time in UTC format to a string as specified by the format argument. The format argument
must be a string.

##Magic Methods:
###__str__():
Returns the local time in string format.

###__bool__():
Returns True if the CityTime object has been set with a local time, otherwise returns false.

###__hash__():
Returns the hash from datetime.datetime set to UTC.

###__eq__():
Returns true if this object's set time in UTC is equal to another CityTime object's UTC time.

For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
object that is set to 5pm in New York on the same date, it will show as equal.

###__ne__():
Returns true if this object's set time in UTC is not equal to another CityTime object's UTC time.

For example, if this object is set to 4pm in Chicago, and you compare it to another CityTime
object that is set to 4pm in New York on the same date, it will show as not equal, because when
it is 4pm in Chicago it is 5pm in New York.

###__lt__():
Returns true if this object's set time in UTC is earlier than another CityTime object's UTC time.

For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
object that is set to 5pm in New York on the same date, it will return True, however if the
same comparison is made when this object is set to 4pm in Chicago, it will return False because when
it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

###__le__():
Returns true if this object's set time in UTC is earlier than or equal to another CityTime
object's UTC time.

For example, if this object is set to 3pm in Chicago, and you compare it to another CityTime
object that is set to 5pm in New York on the same date, it will return True. If the
same comparison is made when this object is set to 4pm in Chicago, it will also return True
because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
this object is set to 5pm in Chicago, the comparison will then return False becaues 5pm in
Chicago is equivalent to 6pm in New York.

###__gt__():
Returns true if this object's set time in UTC is later than another CityTime object's UTC time.

For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
object that is set to 5pm in New York on the same date, it will return True, however if the
same comparison is made when this object is set to 4pm in Chicago, it will return False because when
it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.

###__ge__():
Returns true if this object's set time in UTC is later than or equal to another CityTime
object's UTC time.

For example, if this object is set to 5pm in Chicago, and you compare it to another CityTime
object that is set to 5pm in New York on the same date, it will return True. If the
same comparison is made when this object is set to 4pm in Chicago, it will also return True
because when it is 4pm in Chicago it is 5pm in New York, and thus the times are equal.  When
this object is set to 3pm in Chicago, the comparison will then return False becaues 3pm in
Chicago is equivalent to 4pm in New York.


##There are also three exceptions inherited from pytz:
###AmbiguousTimeError:
Handles the end of Daylight Savings Time, when the local time between 1:00am and 2:00am occurs twice.
At 2:00am, people set their clocks back an hour to 1:00am, and the clock runs from 1:00am through
1:59am twice.

###NonExistentTimeError:
Handles the start of Daylight Savings Time, when the local time between 1:00am and 2:00am is skipped.
At 1:00am, people set their clocks forward an hour to 2:00am, thus the clock never runs through 1:01am
to 1:59am.

###UnknownTimeZoneError:
Raised if the user tries to pass an unknown time zone string (One that is not in the Olson database).
