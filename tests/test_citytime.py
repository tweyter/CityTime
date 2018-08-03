import datetime
import unittest
from calendar import day_name

import hypothesis.strategies as st
import pytz
from hypothesis import given, assume
from hypothesis.extra.datetime import datetimes
from hypothesis.searchstrategy.strategies import OneOfStrategy
from pytz.exceptions import NonExistentTimeError, AmbiguousTimeError
from pytz.exceptions import UnknownTimeZoneError
from pytest import raises

from src.citytime import CityTime, Range

TIMEZONES = pytz.common_timezones


###
# Tests for object initialization
###

def test_uninitialized():
    ct = CityTime(time=None)
    assert str(ct) == 'CityTime object not set yet.'


def test_uninitialized__repr__():
    CityTime().__repr__(), "CityTime object not set yet."


def test_using_unset():
    ct = CityTime()
    with raises(ValueError):
        ct.astimezone('utc')


@given(datetimes())
def test_set_t_zone(dt):
    ct = CityTime()
    ct.set(dt, str(dt.tzinfo))
    assert ct.is_set()
    assert ct.timezone() == str(dt.tzinfo)


@given(datetimes())
def test_set_datetime(dt):
    ct = CityTime(dt, str(dt.tzinfo))
    assert ct.is_set()
    assert ct.utc().tzinfo == pytz.timezone('UTC')
    assert ct.utc() == dt


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_set_with_citytime(dt, tz):
    ct = CityTime(dt, tz)
    test_time = CityTime(time=ct)
    assert test_time == ct


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_set_with_iso_format(dt, tz):
    """

    @type dt: datetime.datetime 
    @type tz: str 
    @return: 
    """
    dt = dt.replace(second=0, microsecond=0)
    sample = CityTime(dt, tz)
    test_time = CityTime(sample.utc().isoformat(), tz)
    assert test_time == sample


@given(
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones)),
    st.sampled_from(list(pytz.common_timezones))
)
def test_reset_tz(dt, tz1, tz2):
    assume(tz1 != tz2)
    sample = CityTime(dt, tz1)
    test_time = CityTime(sample.utc(), tz2)
    test_time.change_tz(tz1)
    assert test_time == sample


###
# Tests of magic methods
###

@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test__str__(dt, tz):
    zone_check = pytz.timezone(tz)
    time_check = zone_check.localize(dt, is_dst=None).astimezone(pytz.utc)
    assert isinstance(time_check, datetime.datetime)

    ct = CityTime(dt, tz)
    result_time, zone = str(ct).split(sep=';')
    assert result_time == time_check.isoformat()
    assert zone == tz


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test__repr__(dt, tz):
    ct = CityTime(dt, tz)
    repr_check = 'CityTime("{}", "{}")'.format(
        ct.utc().isoformat().split(sep='+')[0],
        tz
    )
    assert repr(ct) == repr_check


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_eval__repr__(dt, tz):
    ct = CityTime(dt, tz)
    e = eval(repr(ct))
    assert e == ct


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test__eq__(dt, tz):
    ct1 = CityTime(dt, tz)
    ct2 = CityTime(dt, tz)
    assert ct1 == ct2


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test__eq__to_datetime(dt, tz):
    ct = CityTime(dt, tz)
    utc_time = ct.utc()
    assert ct == utc_time


@given(
    datetimes(timezones=[]),
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones))
)
def test__ne__(dt1, dt2, tz):
    assume(dt1 != dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 != ct2


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test__ne__non_datetime(dt, tz):
    ct = CityTime(dt, tz)
    non_datetime = {}
    assert ct != non_datetime


@given(
    datetimes(timezones=[]),
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones))
)
def test__lt__(dt1, dt2, tz):
    assume(dt1 < dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 < ct2


@given(
    datetimes(timezones=[]),
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones))
)
def test__le__(dt1, dt2, tz):
    assume(dt1 <= dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 <= ct2


@given(
    datetimes(timezones=[]),
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones))
)
def test__gt__(dt1, dt2, tz):
    assume(dt1 > dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 > ct2


@given(
    datetimes(timezones=[]),
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones))
)
def test__ge__(dt1, dt2, tz):
    assume(dt1 >= dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 >= ct2


@given(
    datetimes(timezones=[]),
    st.integers(),
    st.sampled_from(list(pytz.common_timezones))
)
def test__add__(dt1, i, tz):
    assume(-999999999 < i < 999999999)
    td = datetime.timedelta(seconds=i)
    if i > 0:
        assume(dt1 < datetime.datetime.max - td)
    elif i < 0:
        assume(dt1 > datetime.datetime.min - td)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt1, tz)
    ct2.increment(seconds=i)
    assert ct1 + td == ct2
    # check to see that ct1 is not changed, but that the method returned a new CityTime object
    assert ct1 is not ct1 + td


@given(
    datetimes(timezones=[]),
    st.integers(),
    st.sampled_from(list(pytz.common_timezones))
)
def test__sub__(dt1, i, tz):
    assume(-999999999 < i < 999999999)
    td = datetime.timedelta(seconds=i)
    if i > 0:
        assume(dt1 < datetime.datetime.max - td)
    elif i < 0:
        assume(dt1 > datetime.datetime.min - td)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt1, tz)
    ct2.increment(seconds=-i)
    assert ct1 - td == ct2
    assert ct1 - ct2 == td
    # check to see that ct1 is not changed, but that the method returned a new CityTime object
    assert ct1 is not ct1 - td


def test__hash__():
    ct = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    assert ct.__hash__() == ct.utc().__hash__()


def test__bool__():
    ct = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    assert bool(ct) is True


###
# Tests of normal methods
###

@given(datetimes(timezones=[]))
def test_utc(dt):
    ct1 = CityTime(dt, 'utc')
    assert ct1.utc() == dt.replace(tzinfo=pytz.utc)


@given(datetimes(timezones=[]))
def test_utc_tzinfo(dt):
    ct1 = CityTime(dt, 'utc')
    assert ct1.tzinfo() == pytz.utc


@given(datetimes())
def test_local(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.local() == dt


@given(datetimes())
def test_local_timezone(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.timezone() == str(dt.tzinfo)


@given(datetimes())
def test_copy(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    ct2 = ct1.copy()
    assert ct2 == ct1
    assert ct2 is not ct1


@given(datetimes(), st.sampled_from(list(pytz.common_timezones)))
def test_astimezone(dt, tz):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.astimezone(tz) == dt.astimezone(pytz.timezone(tz))


@given(datetimes())
def test_local_minute(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    minutes = dt.hour * 60 + dt.minute
    assert ct1.local_minute() == minutes


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_timezone(dt, tz):
    ct1 = CityTime(dt, tz)
    assert ct1.timezone() == tz


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_tzinfo(dt, tz):
    ct1 = CityTime(dt, tz)
    assert ct1.tzinfo() == pytz.timezone(tz)


@given(datetimes())
def test_weekday(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.weekday() == dt.weekday()


@given(datetimes())
def test_day_name(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    name = day_name[dt.weekday()]
    assert ct1.day_name() == name


@given(datetimes())
def test_day_abbr(dt):
    weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    name = day_name[dt.weekday()]
    assert ct1.day_name() == name
    assert ct1.day_abbr() == weekdays[dt.weekday()]


@given(datetimes())
def test_time_string(dt):
    assume(str(dt.tzinfo) in pytz.common_timezones_set)
    ct1 = CityTime(dt, str(dt.tzinfo))
    time_string = dt.strftime('%H%M')
    assert ct1.time_string() == time_string


@given(
    datetimes(timezones=[]),
    st.sampled_from(list(pytz.common_timezones)),
    st.integers(),
    st.integers(),
    st.integers(),
    st.integers(),
)
def test_increment(dt, tz, d, h, m, s):
    assume(0 < abs(d) < 99999)
    assume(0 < abs(h) < 9999999)
    assume(0 < abs(m) < 999999999)
    assume(0 < abs(s) < 999999999)
    td = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
    if td > datetime.timedelta():
        assume(dt < datetime.datetime.max - td)
    elif td < datetime.timedelta():
        assume(dt > datetime.datetime.min - td)
    ct1 = CityTime(dt, tz)
    ct2 = CityTime(dt, tz)
    ct1.increment(days=d, hours=h, minutes=m, seconds=s)
    assert ct1 != ct2
    assert ct1 - td == ct2


@given(st.sampled_from(['%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X']))
def test_local_strftime(form):
    test_time = CityTime()
    current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    test_time.set(current_time, str(current_time.tzinfo))
    assert test_time.local_strftime(form) == current_time.strftime(form)


@given(st.sampled_from(['%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X']))
def test_utc_strftime(form):
    test_time = CityTime()
    current_time = datetime.datetime.now(pytz.timezone('UTC'))
    test_time.set(current_time, 'UTC')
    utc_test = test_time.utc()
    assert test_time.utc_strftime(form) == utc_test.strftime(form)


def test_today():
    current_time = datetime.datetime.now()
    if current_time.hour == 11 and current_time.minute == 59 and current_time.second > 58:
        raise Exception('Current time could not be tested as it is too close to '
                        'midnight and might be inaccurate.  Please test again.')
    test_time = CityTime.today()
    test_date = datetime.date.today()
    assert test_time.local().date() == test_date


def test_now():
    test_zone = 'America/Chicago'
    test_time = CityTime.now(test_zone)
    test_date = datetime.date.today()
    assert test_time.timezone() == test_zone
    assert test_time.local().date() == test_date


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_epoch(dt, tz):
    ct = CityTime(dt.replace(second=0, microsecond=0), tz)
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('UTC'))
    result = datetime.timedelta(seconds=ct.epoch())
    assert result + epoch == ct.utc()


@given(datetimes(timezones=[]), st.sampled_from(list(pytz.common_timezones)))
def test_offset(dt, zone):
    dt = dt.replace(second=0, microsecond=0)
    ct = CityTime(dt, zone)
    offset = ct.offset()
    assert offset == ct.local_strftime('%z')


###
# Exception handling
###

def test_not_initialized():
    ct = CityTime()
    with raises(ValueError):
        ct.astimezone('utc')


def test_initialize_wrong_type1():
    with raises(TypeError):
        CityTime('int')


def test_initialize_wrong_type2():
    with raises(TypeError):
        CityTime(42)


###
# Magic method error handling
###

def test_err__eq__():
    ct1 = CityTime(datetime.datetime.min, 'UTC')
    ct2 = CityTime(datetime.datetime.max, 'UTC')
    assert not ct1 == ct2


def test_err__eq__2():
    ct = CityTime(datetime.datetime.min, 'UTC')
    assert not ct == 2


def test_err__eq__3():
    ct = CityTime(datetime.datetime.min, 'UTC')
    assert not ct == 'X'


def test_err__eq__4():
    ct = CityTime(datetime.datetime.min, 'UTC')
    assert not ct == {}


def test_err_ne():
    ct1 = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    ct2 = ct1.copy()
    assert not ct1 != ct2


def test_err_ne2():
    ct = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    assert ct != 2.7


def test_err__lt__():
    ct = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    with raises(TypeError):
        # noinspection PyStatementEffect
        ct < 2.5


def test_err__lt__unset():
    ct = CityTime(datetime.datetime(1900, 1, 1, 0, 0), 'UTC')
    with raises(ValueError):
        # noinspection PyStatementEffect
        ct < CityTime()


class NegativeTests(unittest.TestCase):

    def setUp(self):
        self.early_time = datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)
        self.current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.utc = pytz.timezone('utc')
        self.eastern = pytz.timezone('US/Eastern')
        self.ct1 = CityTime()
        self.ct2 = CityTime()
        self.ct3 = CityTime()
        self.sample_timezones = pytz.common_timezones_set

    @given(st.floats())
    def test__le__(self, x):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            # noinspection PyStatementEffect
            self.ct1 <= x

    def test__le_set(self):
        with self.assertRaises(ValueError):
            # noinspection PyStatementEffect
            self.ct1 <= self.ct2

    @given(st.floats())
    def test__gt__(self, x):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            # noinspection PyStatementEffect
            self.ct1 > x

    @given(st.floats())
    def test__ge__(self, x):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            # noinspection PyStatementEffect
            self.ct1 >= x

    @given(st.floats())
    def test_set_dt(self, x):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises((AttributeError, TypeError)):
            self.ct1.set(x, 'US/Eastern')

    def test_set__sub__(self):
        with self.assertRaises(UnknownTimeZoneError):
            self.ct1 - datetime.datetime.now()

    def test_set__sub__other(self):
        with self.assertRaises(TypeError):
            self.ct1 - 2

    @given(st.floats())
    def test_set_tz(self, x):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises((UnknownTimeZoneError, AttributeError)):
            self.ct1.set(self.current_time, x)

    def test_set_unknown_tz(self):
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            self.ct1.set(self.current_time, 'US/Moscow')

    def test_reset_tz_not_str(self):
        self.ct1.set(self.early_time, 'America/New_York')
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            self.ct1.change_tz('23')

    def test_reset_tz_unknown_tz(self):
        self.ct1.set(self.early_time, 'America/New_York')
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            self.ct1.change_tz('US/Moscow')

    @given(st.integers())
    def test_set_date_instead_of_datetime(self, y):
        assume(0 < y < 9999)
        date = datetime.date(y, 1, 1)
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1.set(date, 'US/Eastern')

    def test_set_nonexistent_time(self):
        self.assertRaises(
            NonExistentTimeError,
            self.ct1.set,
            datetime.datetime(2013, 3, 31, 2, 30),
            'Europe/Copenhagen'
        )

    def test_set_ambiguous_time(self):
        self.assertRaises(
            AmbiguousTimeError,
            self.ct1.set,
            datetime.datetime(2014, 11, 2, 1, 30),
            'America/New_York'
        )

    def test_set_utc_datetime(self):
        t = datetime.datetime.now(tz=pytz.timezone('UTC'))
        self.ct1.set(t, time_zone='US/Eastern')
        self.assertEqual(t, self.ct1.utc())

    def test_is_set(self):
        self.assertFalse(self.ct1.is_set())

    def test_is_set_no_timezone(self):
        self.ct1._datetime = self.current_time
        self.assertFalse(self.ct1.is_set())

    def test_check_set(self):
        self.assertRaises(ValueError, self.ct1.check_set)

    def test_check_set_no_timezone(self):
        self.ct1._datetime = self.current_time
        self.assertRaises(ValueError, self.ct1.check_set)

    def test_bool(self):
        self.assertFalse(self.ct1)

    def test_bool_is_true(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1)

    @given(OneOfStrategy(strategies=(st.complex_numbers(), st.text(), st.binary())))
    def test_increment_wrong_type(self, x):
        ct1 = CityTime(self.current_time, 'US/Eastern')
        with self.assertRaises((TypeError, ValueError)):
            ct1.increment(x)

    def test_increment_no_data(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.assertRaises(ValueError, self.ct1.increment)

    def test_increment_non_existant_time(self):
        # See notes in CityTime.increment
        pass

    def test_local_strftime(self):
        formats = ('%B', '%c')
        test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
        test_time = CityTime(test_dt, 'UTC')
        for form in formats:
            self.assertEqual(test_time.local_strftime(form), test_dt.strftime(form))

    def test_utc_strftime(self):
        formats = ('%B', '%c')
        test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
        test_time = CityTime(test_dt, 'UTC')
        for form in formats:
            self.assertEqual(test_time.utc_strftime(form), test_dt.strftime(form))

    def test_today(self):
        """
        I can't think of any failure tests to use here.

        """

    def test_now(self):
        test_zone = ''
        callable_obj = getattr(CityTime, 'now')
        self.assertRaises(ValueError, callable_obj, test_zone)
        test_zone = 'Idontknow/WhereToGo'
        self.assertRaises(UnknownTimeZoneError, callable_obj, test_zone)

    def test_utc(self):
        self.assertRaises(ValueError, self.ct1.utc)

    def test_local(self):
        self.assertRaises(ValueError, self.ct1.local)

    def test_local_minute(self):
        self.assertRaises(ValueError, self.ct1.local_minute)

    def test_timezone(self):
        self.assertRaises(ValueError, self.ct1.timezone)

    def test_tzinfo(self):
        self.assertRaises(ValueError, self.ct1.tzinfo)

    def test_weekday(self):
        self.assertRaises(ValueError, self.ct1.weekday)

    def test_day_name(self):
        self.assertRaises(ValueError, self.ct1.day_name)

    def test_day_abbr(self):
        self.assertRaises(ValueError, self.ct1.day_abbr)

    def test_time_string(self):
        self.assertRaises(ValueError, self.ct1.time_string)

    def test_increment(self):
        with self.assertRaises(ValueError):
            self.ct1.increment(days=1)

    def test_increment2(self):
        with self.assertRaises(ValueError):
            self.ct1.increment(days=1)

    def test_iso_format_bad_tz(self):
        ct = CityTime()
        with self.assertRaises(UnknownTimeZoneError):
            ct.set_iso_format(self.early_time.isoformat(), True)

    def test_iso_format_bad_tz2(self):
        ct = CityTime()
        with self.assertRaises(UnknownTimeZoneError):
            ct.set_iso_format(self.early_time.isoformat(), "Mars")

    def test_iso_format_bad_iso(self):
        ct = CityTime()
        with self.assertRaises(AttributeError):
            ct.set_iso_format(True, "America/New_York")

    def test_iso_format_bad_iso2(self):
        ct = CityTime()
        with self.assertRaises(ValueError):
            ct.set_iso_format('2000-01-01T01:01:01+05:00', "America/New_York")

    def test_epoch_not_set(self):
        with self.assertRaises(ValueError):
            self.ct1.epoch()


# noinspection PyTypeChecker
class RangeTests(unittest.TestCase):
    def setUp(self):
        self.start_time = CityTime(datetime.datetime(2015, 12, 31, 23, 59), 'UTC')
        self.end_time = CityTime(datetime.datetime(2016, 1, 1, 0, 1), 'UTC')

    def test_empty_init(self):
        r = Range()
        self.assertEqual(r._members, set())

    def test_full_init(self):
        r = Range(self.start_time, self.end_time)
        self.assertNotEqual(r._members, set())

    def test_wrong_init(self):
        ve = ValueError(
                'Range object requires two parameters, either <CityTime, CityTime> or <CityTime, datetime.timedelta>'
            )
        with self.assertRaises(ValueError) as cm:
            Range(2)
        self.assertEqual(
            cm.exception.args,
            ve.args
        )

    def test_create_range(self):
        r = Range()
        r._create_range(self.start_time, self.end_time)
        self.assertEqual(r._members, {self.start_time, self.end_time})

    def test_create_range_not_city_time(self):
        r = Range()
        self.assertRaises(ValueError, r._create_range, self.start_time, 2)

    def test_create_range_city_time_not_set(self):
        r = Range()
        self.assertRaises(ValueError, r._create_range, self.start_time, CityTime())

    def test_start_time(self):
        r = Range(self.end_time, self.start_time)  # purposely reversing the order
        self.assertEqual(r.start_time(), self.start_time)

    def test_end_time(self):
        r = Range(self.end_time, self.start_time)  # purposely reversing the order
        self.assertEqual(r.end_time(), self.end_time)

    def test_create_range_timedelta(self):
        r = Range()
        r._create_range_timedelta(self.start_time, datetime.timedelta(minutes=1))
        check = map(lambda x: isinstance(x, CityTime), r._members)
        self.assertTrue(all(check))

    def test_create_range_timedelta_using_init(self):
        r = Range(self.start_time, datetime.timedelta(minutes=1))
        check = map(lambda x: isinstance(x, CityTime), r._members)
        self.assertTrue(all(check))

    def test_create_range_bad_data(self):
        r = Range()
        self.assertRaises(ValueError, r._create_range_timedelta, 2, datetime.timedelta())
        self.assertRaises(ValueError, r._create_range_timedelta, CityTime(), datetime.timedelta())
        self.assertRaises(ValueError, r._create_range_timedelta, self.start_time, 2)

    def test_check_set(self):
        r = Range(self.start_time, self.end_time)
        self.assertTrue(r.check_set())

    def test_check_set_false(self):
        r = Range()
        self.assertFalse(r.check_set())

    def test_delta(self):
        """
        Test for the delta method which calculates the timedelta between start time and
        end time.

        start_time and end_time must be set to CityTime objects, and each
        CityTime object must be set to a valid time.

        The method should return a valid datetime.timedelta.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        self.assertEqual(r.delta(), self.end_time - self.start_time)

    def test_delta_not_set(self):
        r = Range()
        self.assertEqual(r.delta(), datetime.timedelta())

    def test_contains_range(self):
        """
        Test for the contains method which determines if the start and end times of
        one Range object fall entirely within the start and end times of another
        Range object.

        Assumes that both Range objects are set with valid CityTimes.
        The contains method should return a boolean.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        contained = Range(self.start_time, self.end_time)
        self.assertTrue(r.contains(contained))

    def test_contains_citytime(self):
        """
        Test for the contains method to see that it can also test for
        an individual CityTime object to be contained within the range.
        @return:
        """

        r = Range(self.start_time, self.end_time)
        contained = self.start_time
        self.assertTrue(r.contains(contained))

    def test_contains_false(self):
        r = Range(self.start_time, self.end_time)
        not_contained = Range(self.end_time, datetime.timedelta(hours=-1))
        self.assertFalse(r.contains(not_contained))

    def test_contains_errors(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            r.contains(self.start_time)
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test_contains_errors2(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.contains(Range())
        self.assertEqual(cm.exception.args, ('Object to be compared is not set.',))

    def test_contains_none(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r.contains(None))

    def test_contains_outside_of_range(self):
        r = Range(self.start_time, self.end_time)
        t = self.start_time.copy()
        t.increment(days=-1)
        self.assertFalse(r.contains(t))

    def test_overlaps(self):
        """
        Test for the overlaps method which determines if either the start time
        or end time of another Range object falls within the range of the current
        Range object.

        Assumes that both Range objects are set with valid CityTimes.
        The overlaps method should return a boolean.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        overlap_range = Range(self.start_time, datetime.timedelta(days=100))
        self.assertTrue(r.overlaps(overlap_range))

    def test_overlaps_start_time(self):
        """
        Similar test to test_overlaps, but this time we overlap the start time instead
        of the end time.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        overlap_range = Range(self.end_time, datetime.timedelta(days=-100))
        self.assertTrue(r.overlaps(overlap_range))

    def test_overlaps_with_contained_range(self):
        """
        Another test of the overlaps method, but with a range that is entirely
        contained within the Range object.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        overlap_range = Range(self.start_time, self.end_time)
        self.assertTrue(r.overlaps(overlap_range))

    def test_overlaps_false(self):
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(days=-1)
        non_overlap = Range(new_start_time, datetime.timedelta(hours=1))
        self.assertFalse(r.overlaps(non_overlap))

    def test_overlaps_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            r.overlaps(True)
        self.assertEqual(cm.exception.args, ("Object to be compared must be of type 'Range'",))

    def test_overlaps_not_set(self):
        r = Range()
        cr = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.overlaps(cr)
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test_overlaps_param_not_set(self):
        cr = Range()
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.overlaps(cr)
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test_overlaps_param_is_none(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r.overlaps(None))

    def test_overlap(self):
        """
        Test for the overlap method, which determines how much of one Range object
        overlaps with another Range object.

        Assumes that both Range objects are set with valid CityTimes.
        The overlap method should return a datetime.timedelta.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        overlap_range = Range(self.start_time, datetime.timedelta(days=100))
        self.assertEqual(r.overlap(overlap_range), r.delta())

    def test_overlap_start_time(self):
        """
        Similar to test_overlap, but tests a trip that overlaps the start_time
        of the base Range object.

        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(hours=-100)
        overlap_range = Range(new_start_time, self.end_time)
        self.assertEqual(r.overlap(overlap_range), r.delta())

    def test_not_overlapping(self):
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(days=-1)
        non_overlap = Range(new_start_time, datetime.timedelta(hours=1))
        self.assertEqual(r.overlap(non_overlap), datetime.timedelta())

    def test_overlap_not_set(self):
        r = Range()
        cr = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.overlap(cr)
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test_overlap_param_not_set(self):
        cr = Range()
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.overlap(cr)
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test_same_as(self):
        """
        Test of equality that returns True if both start times and end times are
        equal to each other.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        equals = Range(self.start_time, self.end_time)
        self.assertTrue(r == equals)

    def test_not_same(self):
        """
        Test of inequality between Range objects.

        Returns True if either the start_times don't match or the end_times don't match.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=1)
        equals = Range(new_start_time, self.end_time)
        self.assertTrue(r != equals)

    def test_before(self):
        r = Range(self.start_time, self.end_time)
        new_end_time = self.end_time.copy()
        new_end_time.increment(hours=-1)
        lesser = Range(new_end_time, new_end_time)
        self.assertTrue(lesser.before(r))

    def test_before_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            r.before(2)
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test_before_not_set(self):
        r = Range()
        cr = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.before(cr)
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test_before_param_not_set(self):
        cr = Range()
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.before(cr)
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test_after(self):
        r = Range(self.start_time, self.end_time)
        new_end_time = self.end_time.copy()
        new_end_time.increment(hours=-1)
        lesser = Range(new_end_time, new_end_time)
        self.assertTrue(r.after(lesser))

    def test_after_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            r.after(2)
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test_after_not_set(self):
        r = Range()
        cr = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.after(cr)
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test_after_param_not_set(self):
        cr = Range()
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            r.after(cr)
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__eq__(self):
        r = Range(self.start_time, self.end_time)
        s = Range(self.start_time, self.end_time)
        self.assertTrue(r == s)

    def test__eq__not_range(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r == 3)

    def test__eq__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r == r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__eq__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r == Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__eq__false(self):
        r = Range(self.start_time, self.end_time)
        cr = r.copy()
        cr.extend_prior(datetime.timedelta(seconds=1))
        self.assertFalse(r == cr)

    def test__ne__(self):
        r = Range(self.start_time, self.end_time)
        s = r.copy()
        s.extend(datetime.timedelta(seconds=1))
        self.assertTrue(r != s)

    def test__ne__not_range(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            # noinspection PyStatementEffect
            r != 3
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test__ne__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r != r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__ne__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r != Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__ne__false(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r != r)

    def test__lt__(self):
        r = Range(self.start_time, self.end_time)
        s = r.copy()
        s.extend(datetime.timedelta(seconds=1))
        self.assertTrue(r < s)

    def test__lt__not_range(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            # noinspection PyStatementEffect
            r < 3
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test__lt__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r < r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__lt__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r < Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__lt__false(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r < r)

    def test__le__(self):
        r = Range(self.start_time, self.end_time)
        s = r.copy()
        self.assertTrue(r <= s)
        s.extend(datetime.timedelta(seconds=1))
        self.assertTrue(r <= s)

    def test__le__not_range(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            # noinspection PyStatementEffect
            r <= 3
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test__le__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r <= r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__le__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r <= Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__le__false(self):
        r = Range(self.start_time, self.end_time)
        cr = r.copy()
        r.extend(datetime.timedelta(seconds=1))
        self.assertFalse(r <= cr)

    def test__gt__(self):
        r = Range(self.start_time, self.end_time)
        s = r.copy()
        s.extend(datetime.timedelta(seconds=1))
        self.assertTrue(s > r)

    def test__gt__not_range(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            # noinspection PyStatementEffect
            r > 3
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test__gt__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r > r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__gt__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r > Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__gt__false(self):
        r = Range(self.start_time, self.end_time)
        self.assertFalse(r > r)

    def test__ge__(self):
        r = Range(self.start_time, self.end_time)
        s = r.copy()
        self.assertTrue(s >= r)
        s.extend(datetime.timedelta(seconds=1))
        self.assertTrue(s >= r)

    def test__ge__not_range(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(TypeError) as cm:
            # noinspection PyStatementEffect
            r >= 3
        self.assertEqual(cm.exception.args, ("unorderable types: Range, <class 'int'>",))

    def test__ge__not_set(self):
        r = Range()
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r >= r
        self.assertEqual(cm.exception.args, ('Range is not set.',))

    def test__ge__other_not_set(self):
        r = Range(self.start_time, self.end_time)
        with self.assertRaises(ValueError) as cm:
            # noinspection PyStatementEffect
            r >= Range()
        self.assertEqual(cm.exception.args, ('Range object to be compared is not set.',))

    def test__ge__false(self):
        r = Range(self.start_time, self.end_time)
        cr = r.copy()
        r.extend(datetime.timedelta(seconds=1))
        self.assertFalse(cr >= r)

    def test__str__(self):
        r = Range(self.start_time, self.end_time)
        self.assertEqual(
            r.__str__(),
            "Range: start: {} - end: {}".format(
                self.start_time.__str__(),
                self.end_time.__str__()
            )
        )

    def test__repr__(self):
        r = Range(self.start_time, self.end_time)
        self.assertEqual(
            r.__repr__(),
            "Range: start: {} - end: {}".format(
                self.start_time.__str__(),
                self.end_time.__str__()
            )
        )

    def test__bool__(self):
        r = Range()
        self.assertFalse(r)

    def test_extend(self):
        """
        Test for the extend method, which extends (ie. sets to a later time)
        the end_time of the Range object by the given timedelta.

        Assumes that the argument is a datetime.timedelta and that its value is positive.
        Assumes that the Range object is set.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        delta = r.delta()
        extension = datetime.timedelta(days=1)
        r.extend(extension)
        self.assertEqual(r.delta(), delta + extension)

    def test_extend_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        self.assertRaises(TypeError, r.extend, 2)

    def test_extend_negative_delta(self):
        r = Range(self.start_time, self.end_time)
        delta = datetime.timedelta(days=-1)
        self.assertRaises(ValueError, r.extend, delta)

    def test_extend_not_set(self):
        r = Range()
        delta = datetime.timedelta(days=-1)
        self.assertRaises(ValueError, r.extend, delta)

    def test_extend_prior(self):
        """
        Test for the extend_prior method, which extends (ie. sets to an earlier time)
        the start_time of the Range object by the given timedelta.

        Assumes that the argument is a datetime.timedelta and that its value is positive.
        Assumes that the Range object is set.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        delta = r.delta()
        extension = datetime.timedelta(days=1)
        r.extend_prior(extension)
        self.assertEqual(r.delta(), delta + extension)

    def test_extend_prior_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        self.assertRaises(TypeError, r.extend_prior, 2)

    def test_extend_prior_negative_delta(self):
        r = Range(self.start_time, self.end_time)
        delta = datetime.timedelta(days=-1)
        self.assertRaises(ValueError, r.extend_prior, delta)

    def test_extend_prior_not_set(self):
        r = Range()
        delta = datetime.timedelta(days=-1)
        self.assertRaises(ValueError, r.extend_prior, delta)

    def test_replace_start_time(self):
        """
        Test for the replace_start_time method, which alters the current Range object
        by assigning it a new start_time value.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=1)
        r.replace_start_time(new_start_time)
        self.assertEqual(r, Range(new_start_time, self.end_time))

    def test_replace_start_time_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        self.assertRaises(TypeError, r.replace_start_time, 2)

    def test_replace_start_time_not_set(self):
        r = Range()
        self.assertRaises(ValueError, r.replace_start_time, self.start_time)

    def test_replace_end_time(self):
        """
        Test for the replace_end_time method, which alters the current Range object
        by assigning it a new end_time value.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_end_time = self.end_time.copy()
        new_end_time.increment(minutes=1)
        r.replace_end_time(new_end_time)
        self.assertEqual(r, Range(self.start_time, new_end_time))

    def test_replace_end_time_end_type(self):
        r = Range(self.start_time, self.end_time)
        self.assertRaises(TypeError, r.replace_end_time, 2)

    def test_replace_end_time_not_set(self):
        r = Range()
        self.assertRaises(ValueError, r.replace_end_time, self.start_time)

    def test_intersection(self):
        """
        Test for the intersection method, which creates a new Range object out of the
        where the two Range objects overlap.

        Assumes that both Range objects are set with valid CityTimes.
        The intersection method should return a new Range object.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.end_time.copy()
        new_start_time.increment(minutes=-1)
        new_end_time = self.end_time.copy()
        new_end_time.increment(minutes=1)
        intersector = Range(new_start_time, new_end_time)
        self.assertEqual(
            r.intersection(intersector),
            Range(new_start_time, self.end_time)
        )

    def test_intersection_contained(self):
        """
        Test for a range that is smaller than, and entirely contained within,
        the current object.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time
        new_start_time.increment(minutes=1)
        new_end_time = self.end_time
        new_end_time.increment(minutes=-1)
        contained = Range(new_start_time, new_end_time)
        self.assertEqual(r.intersection(contained), contained)

    def test_intersection__gt__(self):
        """
        Test to see that a Range object that is entirely outside of (greater than)
        the current object returns a value of None.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.end_time.copy()
        new_start_time.increment(minutes=1)
        greater = Range(new_start_time, new_start_time)
        self.assertIsNone(r.intersection(greater))

    def test_intersection__lt__(self):
        """
        Test to see that a Range object that is entirely outside of (less than)
        the current object returns a value of None.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=-1)
        lesser = Range(new_start_time, new_start_time)
        self.assertIsNone(r.intersection(lesser))

    def test_intersection_not_set(self):
        r = Range()
        nr = Range(self.start_time, self.end_time)
        self.assertRaises(ValueError, r.intersection, nr)

    def test_intersection_other_not_set(self):
        r = Range()
        nr = Range(self.start_time, self.end_time)
        self.assertRaises(ValueError, nr.intersection, r)

    def test_intersection_contained_in_other(self):
        """
        Test for the intersection method, when the Range object is contained entirely
        within the Range object given in the parameter.

        @return:
        """
        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=-1)
        new_end_time = self.end_time.copy()
        new_end_time.increment(minutes=1)
        intersector = Range(new_start_time, new_end_time)
        self.assertEqual(
            r.intersection(intersector),
            r
        )

    def test_intersection_overlaps_start_time(self):

        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=-1)
        new_end_time = self.end_time.copy()
        new_end_time.increment(minutes=-1)
        intersector = Range(new_start_time, new_end_time)
        self.assertEqual(
            r.intersection(intersector),
            Range(self.start_time, new_end_time)
        )

    def test_intersection_overlaps_end_time(self):

        r = Range(self.start_time, self.end_time)
        new_start_time = self.start_time.copy()
        new_start_time.increment(minutes=1)
        new_end_time = self.end_time.copy()
        new_end_time.increment(minutes=1)
        intersector = Range(new_start_time, new_end_time)
        self.assertEqual(
            r.intersection(intersector),
            Range(new_start_time, self.end_time)
        )

    def test_copy(self):
        """
        Test of the copy method, which returns a deep copy of the Range instance.
        @return:
        """
        r = Range(self.start_time, self.end_time)
        copied = r.copy()

        # Check to see that the two objects have the same value
        self.assertEqual(r, copied)

        # Check to see that they are unique objects.
        self.assertNotEqual(id(r), id(copied))

        # Check to see that the start_times are unique objects
        self.assertNotEqual(id(r.start_time()), id(copied.start_time()))

        # Check to see that the end_times are unique objects
        self.assertNotEqual(id(r.end_time()), id(copied.end_time()))

    def test_copy_not_set(self):
        r = Range()
        self.assertRaises(ValueError, r.copy)

    def test_shift(self):
        r = Range(self.start_time, self.end_time)
        start_check = self.start_time.copy()
        start_check.increment(days=1)
        end_check = self.end_time.copy()
        end_check.increment(days=1)
        r.shift(datetime.timedelta(days=1))
        self.assertEqual(r.start_time(), start_check)
        self.assertEqual(r.end_time(), end_check)

    def test_shift_wrong_type(self):
        r = Range(self.start_time, self.end_time)
        self.assertRaises(TypeError, r.shift, 2)


class RangeHypothesisTests(unittest.TestCase):

    @given(datetimes(timezones=[]), datetimes(timezones=[]))
    def test__init__(self, dt, dt2):
        assume(dt <= dt2)
        start_time = CityTime(dt, 'UTC')
        end_time = CityTime(dt2, 'UTC')
        r1 = Range(start_time, end_time)
        self.assertEqual(r1._members, {start_time, end_time})

    @given(datetimes(timezones=[]), st.integers())
    def test__init__timedelta(self, dt, delta):
        assume(overflow(dt, delta))
        start_time = CityTime(dt, 'UTC')
        td = datetime.timedelta(seconds=delta)
        end_time = CityTime(dt, 'UTC')
        end_time.increment(seconds=delta)
        r = Range(start_time, td)
        self.assertEqual(r._members, {start_time, end_time})

    @given(datetimes(timezones=[]), datetimes(timezones=[]))
    def test_start_time(self, start, end):
        assume(start <= end)
        start_time = CityTime(start, 'UTC')
        r = Range(start_time, CityTime(end, 'UTC'))
        self.assertEqual(start_time, r.start_time())

    @given(datetimes(timezones=[]), datetimes(timezones=[]))
    def test_end_time(self, start, end):
        assume(start <= end)
        end_time = CityTime(start, 'UTC')
        r = Range(CityTime(end, 'UTC'), end_time)
        self.assertEqual(end_time, r.start_time())

    @given(datetimes(timezones=[]), st.integers())
    def test_delta(self, dt, delta):

        assume(overflow(dt.replace(microsecond=0), delta))
        start_time = CityTime(dt.replace(microsecond=0), 'UTC')
        td = datetime.timedelta(seconds=delta)
        r = Range(start_time, td)
        if delta >= 0:
            self.assertEqual(r.delta(), td)
        else:
            self.assertEqual(r.delta(), -td)

    @given(datetimes(timezones=[]), st.integers(min_value=0), st.integers(min_value=0))
    def test_contains(self, dt, delta1, delta2):
        time = dt.replace(microsecond=0)
        assume(overflow(time, delta1))
        assume(delta2 <= delta1)
        start_time = CityTime(time, 'UTC')
        td1 = datetime.timedelta(seconds=delta1)
        td2 = datetime.timedelta(seconds=delta2)
        r1 = Range(start_time, td1)
        end_time = r1.end_time()
        r2 = Range(start_time, td2)
        self.assertRaises(TypeError, r1.contains, str())
        if delta1 == delta2:
            self.assertTrue(r1.contains(r2))
            self.assertTrue(r2.contains(r1))
            return
        self.assertTrue(r1.contains(r2))
        self.assertFalse(r2.contains(r1))
        r3 = Range(end_time, -td2)
        self.assertTrue(r1.contains(r3))
        self.assertFalse(r3.contains(r1))

    @given(datetimes(timezones=[]), st.integers(min_value=0), st.integers(min_value=0))
    def test_overlaps(self, dt, delta1, delta2):
        time = dt.replace(microsecond=0)
        assume(overflow(time, delta1))
        assume(overflow(time, delta1 - delta2))
        start_time = CityTime(time, 'UTC')
        td1 = datetime.timedelta(seconds=delta1)
        td2 = datetime.timedelta(seconds=delta2)
        r1 = Range(start_time, td1)
        r2 = Range(start_time, td2)
        self.assertTrue(r1.overlaps(r2))
        self.assertTrue(r2.overlaps(r1))

    @given(datetimes(timezones=[]), st.integers(min_value=0), st.integers(min_value=0))
    def test_overlaps2(self, dt, delta1, delta2):
        time = dt.replace(microsecond=0)
        assume(overflow(time, delta1))
        assume(overflow(time, delta1 - delta2))
        start_time = CityTime(time, 'UTC')
        td1 = datetime.timedelta(seconds=delta1)
        td2 = datetime.timedelta(seconds=delta2)
        r1 = Range(start_time, td1)
        end_time = r1.end_time()
        r3 = Range(end_time, -td2)
        self.assertTrue(r1.overlaps(r3))
        self.assertTrue(r3.overlaps(r1))

    @given(datetimes(timezones=[]), datetimes(timezones=[]), st.integers(min_value=0), st.integers(max_value=0))
    def test_overlaps_false(self, dt1, dt2, delta1, delta2):
        assume(dt1 > dt2)
        assume(overflow(dt1, delta1))
        assume(overflow(dt2, delta2))
        r1 = Range(CityTime(dt1, 'UTC'), datetime.timedelta(seconds=delta1))
        r2 = Range(CityTime(dt2, 'UTC'), datetime.timedelta(seconds=delta2))
        self.assertFalse(r1.overlaps(None))
        self.assertFalse(r1.overlaps(r2))
        self.assertFalse(r2.overlaps(r1))

    @given(datetimes(timezones=[]), st.integers(min_value=0), st.integers(min_value=0))
    def test_overlap(self, dt, delta1, delta2):
        time = dt.replace(microsecond=0)
        assume(overflow(time, delta1))
        assume(delta2 < delta1)
        start_time = CityTime(time, 'UTC')
        td1 = datetime.timedelta(seconds=delta1)
        td2 = datetime.timedelta(seconds=delta2)
        r1 = Range(start_time, td1)
        end_time = r1.end_time()
        r2 = Range(start_time, td2)
        self.assertEqual(r2.delta(), r1.overlap(r2))
        self.assertEqual(r2.delta(), r1.overlap(r2))
        r3 = Range(end_time, -td2)
        self.assertEqual(r2.delta(), r1.overlap(r3))
        self.assertEqual(r2.delta(), r3.overlap(r1))

    @given(st.integers(min_value=0))
    def test_timedelta_to_h_mm(self, d):
        assume(overflow(
            datetime.datetime(1970, 1, 1, 0, 0),
            d * 60)
        )
        delta = datetime.timedelta(minutes=d)
        start_time = CityTime(datetime.datetime(1970, 1, 1, 0, 0), 'UTC')
        rng = Range(start_time, delta)
        h, mm = divmod(int(delta.total_seconds()), 3600)
        m, _ = divmod(mm, 60)
        assert rng.timedelta_to_h_mm() == '{0:01d}:{1:02d}'.format(h, m)


def overflow(date_time, time_delta):
    try:
        date_time + datetime.timedelta(seconds=time_delta)
    except OverflowError:
        return False
    else:
        return True


def timezones():  # pragma: no cover
    return pytz.common_timezones


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
