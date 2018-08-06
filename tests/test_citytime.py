import datetime
import unittest
from calendar import day_name

import hypothesis.strategies as st
import pytz
from hypothesis import given, assume
from hypothesis.strategies import datetimes
from hypothesis.extra.pytz import timezones as t_zones
from pytest import raises

from citytime import CityTime

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


@given(datetimes(timezones=t_zones()))
def test_set_t_zone(dt):
    ct = CityTime()
    ct.set(dt, str(dt.tzinfo))
    assert ct.is_set()
    assert ct.timezone() == str(dt.tzinfo)


@given(datetimes(timezones=t_zones()))
def test_set_datetime(dt):
    ct = CityTime(dt, str(dt.tzinfo))
    assert ct.is_set()
    assert ct.utc().tzinfo == pytz.timezone('UTC')
    assert ct.utc() == dt


@given(datetimes(timezones=t_zones()))
def test_set_with_citytime(dt):
    ct = CityTime(dt, str(dt.tzinfo))
    test_time = CityTime(time=ct)
    assert test_time == ct


@given(datetimes(timezones=t_zones()))
def test_set_with_iso_format(dt):
    dt = dt.replace(second=0, microsecond=0)
    sample = CityTime(dt, str(dt.tzinfo))
    test_time = CityTime(sample.utc().isoformat(), str(dt.tzinfo))
    assert test_time == sample


@given(
    datetimes(timezones=t_zones()),
    t_zones(),
)
def test_reset_tz(dt, tz2):
    assume(str(dt.tzinfo) != str(tz2))
    sample = CityTime(dt, str(dt.tzinfo))
    test_time = CityTime(sample.utc(), str(tz2))
    test_time.change_tz(str(dt.tzinfo))
    assert test_time == sample


###
# Tests of magic methods
###

@given(datetimes(timezones=t_zones()))
def test__str__(dt):
    tz = str(dt.tzinfo)
    # time_check = dt.tzinfo.localize(dt, is_dst=None).astimezone(pytz.utc)
    # assert isinstance(time_check, datetime.datetime)

    ct = CityTime(dt, tz)
    result_time, zone = str(ct).split(sep=';')
    compare = pytz.timezone('UTC').normalize(dt).isoformat()
    assert compare == result_time
    assert tz == zone


@given(datetimes(timezones=t_zones()))
def test__repr__(dt):
    tz = str(dt.tzinfo)
    ct = CityTime(dt, tz)
    repr_check = 'CityTime("{}", "{}")'.format(
        ct.utc().isoformat().split(sep='+')[0],
        tz
    )
    assert repr_check == repr(ct)


@given(datetimes(timezones=t_zones()))
def test_eval__repr__(dt):
    tz = str(dt.tzinfo)
    ct = CityTime(dt, tz)
    e = eval(repr(ct))
    assert e == ct


@given(datetimes(timezones=t_zones()))
def test__eq__(dt):
    tz = str(dt.tzinfo)
    ct1 = CityTime(dt, tz)
    ct2 = CityTime(dt, tz)
    assert ct1 == ct2


@given(
    datetimes(timezones=st.none()),
    datetimes(timezones=st.none()),
    st.sampled_from(list(pytz.common_timezones))
)
def test__ne__(dt1, dt2, tz):
    assume(dt1 != dt2)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt2, tz)
    assert ct1 != ct2


@given(datetimes(timezones=t_zones()))
def test__ne__non_datetime(dt):
    tz = str(dt.tzinfo)
    ct = CityTime(dt, tz)
    non_datetime = {}
    assert ct != non_datetime


@given(
    datetimes(timezones=t_zones()),
    datetimes(timezones=t_zones()),
)
def test__lt__(dt1, dt2):
    assume(dt1 < dt2)
    ct1 = CityTime(dt1, str(dt1.tzinfo))
    ct2 = CityTime(dt2, str(dt2.tzinfo))
    assert ct1 < ct2


@given(
    datetimes(timezones=t_zones()),
    datetimes(timezones=t_zones()),
)
def test__le__(dt1, dt2):
    assume(dt1 <= dt2)
    ct1 = CityTime(dt1, str(dt1.tzinfo))
    ct2 = CityTime(dt2, str(dt2.tzinfo))
    assert ct1 <= ct2


@given(
    datetimes(timezones=t_zones()),
    datetimes(timezones=t_zones()),
)
def test__gt__(dt1, dt2):
    assume(dt1 > dt2)
    ct1 = CityTime(dt1, str(dt1.tzinfo))
    ct2 = CityTime(dt2, str(dt2.tzinfo))
    assert ct1 > ct2


@given(
    datetimes(timezones=t_zones()),
    datetimes(timezones=t_zones()),
)
def test__ge__(dt1, dt2):
    assume(dt1 >= dt2)
    ct1 = CityTime(dt1, str(dt1.tzinfo))
    ct2 = CityTime(dt2, str(dt2.tzinfo))
    assert ct1 >= ct2


@given(
    datetimes(timezones=t_zones()),
    st.integers(min_value=-999999999, max_value=999999999),
)
def test__add__(dt1, i):
    tz = str(dt1.tzinfo)
    td = datetime.timedelta(seconds=i)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt1, tz)
    try:
        ct2.increment(seconds=i)
    except OverflowError:
        assume(False)
    assert ct1 + td == ct2
    # check to see that ct1 is not changed, but that the method returned a new CityTime object
    assert ct1 is not ct1 + td


@given(
    datetimes(timezones=t_zones()),
    st.integers(min_value=-999999999, max_value=999999999),
)
def test__sub__(dt1, i):
    tz = str(dt1.tzinfo)
    td = datetime.timedelta(seconds=i)
    ct1 = CityTime(dt1, tz)
    ct2 = CityTime(dt1, tz)
    try:
        ct2.increment(seconds=-i)
    except OverflowError:
        assume(False)
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

@given(datetimes(timezones=st.none()))
def test_utc(dt):
    ct1 = CityTime(dt, 'utc')
    assert ct1.utc() == dt.replace(tzinfo=pytz.utc)


@given(datetimes(timezones=st.none()))
def test_utc_tzinfo(dt):
    ct1 = CityTime(dt, 'utc')
    assert ct1.tzinfo() == pytz.utc


@given(datetimes(timezones=t_zones()))
def test_local(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.local() == dt


@given(datetimes(timezones=t_zones()))
def test_local_timezone(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.timezone() == str(dt.tzinfo)


@given(datetimes(timezones=t_zones()))
def test_copy(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    ct2 = ct1.copy()
    assert ct2 == ct1
    assert ct2 is not ct1


@given(datetimes(timezones=t_zones()), st.sampled_from(list(pytz.common_timezones)))
def test_astimezone(dt, tz):
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.astimezone(tz) == dt.astimezone(pytz.timezone(tz))


@given(datetimes(timezones=t_zones()))
def test_local_minute(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    minutes = dt.hour * 60 + dt.minute
    assert ct1.local_minute() == minutes


@given(datetimes(timezones=t_zones()))
def test_timezone(dt):
    tz = str(dt.tzinfo)
    ct1 = CityTime(dt, tz)
    assert ct1.timezone() == str(pytz.timezone(tz))


@given(datetimes(timezones=t_zones()))
def test_tzinfo(dt):
    tz = str(dt.tzinfo)
    ct1 = CityTime(dt, tz)
    assert ct1.tzinfo() == pytz.timezone(tz)


@given(datetimes(timezones=t_zones()))
def test_weekday(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    assert ct1.weekday() == dt.weekday()


@given(datetimes(timezones=t_zones()))
def test_day_name(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    name = day_name[dt.weekday()]
    assert ct1.day_name() == name


@given(datetimes(timezones=t_zones()))
def test_day_abbr(dt):
    weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    ct1 = CityTime(dt, str(dt.tzinfo))
    name = day_name[dt.weekday()]
    assert ct1.day_name() == name
    assert ct1.day_abbr() == weekdays[dt.weekday()]


@given(datetimes(timezones=t_zones()))
def test_time_string(dt):
    ct1 = CityTime(dt, str(dt.tzinfo))
    time_string = dt.strftime('%H%M')
    assert ct1.time_string() == time_string


@given(
    datetimes(timezones=t_zones()),
    st.integers(min_value=0, max_value=99999),
    st.integers(min_value=0, max_value=9999999),
    st.integers(min_value=0, max_value=999999999),
    st.integers(min_value=1, max_value=999999999),
)
def test_increment(dt, d, h, m, s):
    tz = str(dt.tzinfo)
    td = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
    ct1 = CityTime(dt, tz)
    ct2 = CityTime(dt, tz)
    try:
        ct1.increment(days=d, hours=h, minutes=m, seconds=s)
    except OverflowError:
        assume(False)
    assert ct1 != ct2
    assert ct1 - td == ct2


@given(
    datetimes(timezones=t_zones()),
    st.sampled_from(['%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X']),
)
def test_local_strftime(dt, form):
    test_time = CityTime(dt, str(dt.tzinfo))
    assert test_time.local_strftime(form) == dt.strftime(form)


@given(
    datetimes(timezones=t_zones()),
    st.sampled_from(['%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X']),
)
def test_utc_strftime(dt, form):
    test_time = CityTime(dt, str(dt.tzinfo))
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


@given(datetimes(timezones=t_zones()))
def test_epoch(dt):
    tz = str(dt.tzinfo)
    ct = CityTime(dt.replace(second=0, microsecond=0), tz)
    epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('UTC'))
    result = datetime.timedelta(seconds=ct.epoch())
    assert result + epoch == ct.utc()


@given(datetimes(timezones=t_zones()))
def test_offset(dt):
    tz = str(dt.tzinfo)
    dt = dt.replace(second=0, microsecond=0)
    ct = CityTime(dt, tz)
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
