CityTime
========

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

A CityTime object can be instantiated using a datetime.datetime object, an ISO8601 string, or another
CityTime object. If instantiated using an ISO8601 string, the time used must be UTC, it will not work
with a localized time.