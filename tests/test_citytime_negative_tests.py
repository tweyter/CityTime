import datetime

import hypothesis.strategies as st
import pytz
from hypothesis import given
from hypothesis.searchstrategy.strategies import OneOfStrategy
from pytz.exceptions import NonExistentTimeError, AmbiguousTimeError
from pytz.exceptions import UnknownTimeZoneError
import pytest

from citytime import CityTime

EARLY_TIME = datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)


def test__le__():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises(TypeError):
        # noinspection PyStatementEffect
        dt <= 3.14


def test__le_set():
    with pytest.raises(ValueError):
        # noinspection PyStatementEffect
        CityTime() <= CityTime()


def test__gt__():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises(TypeError):
        # noinspection PyStatementEffect
        dt > 3.14


def test__ge__():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises(TypeError):
        # noinspection PyStatementEffect
        dt >= 3.14


def test_set_dt():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises((AttributeError, TypeError)):
        dt.set(3.14, 'US/Eastern')


def test_set__sub__():
    with pytest.raises(UnknownTimeZoneError):
        CityTime() - datetime.datetime.now()


def test_set__sub__other():
    with pytest.raises(TypeError):
        CityTime() - 2


def test_set_tz():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises((UnknownTimeZoneError, AttributeError)):
        dt.set(datetime.datetime(2018, 1, 1, 10, 0), 3.14)


def test_set_unknown_tz():
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        CityTime(datetime.datetime(2018, 1, 1, 10, 0), 'US/Moscow')


def test_reset_tz_not_str():
    dt = CityTime(EARLY_TIME, 'America/New_York')
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        dt.change_tz('23')


def test_reset_tz_unknown_tz():
    dt = CityTime(EARLY_TIME, 'America/New_York')
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        dt.change_tz('US/Moscow')


def test_set_date_instead_of_datetime():
    dt = CityTime(EARLY_TIME, 'US/Eastern')
    with pytest.raises(TypeError):
        dt.set(datetime.date(2018, 1, 1), 'US/Eastern')


def test_set_nonexistent_time():
    with pytest.raises(NonExistentTimeError):
        CityTime(datetime.datetime(2013, 3, 31, 2, 30), 'Europe/Copenhagen')


def test_set_ambiguous_time():
    with pytest.raises(AmbiguousTimeError):
        CityTime(datetime.datetime(2014, 11, 2, 1, 30), 'America/New_York')


def test_is_set():
    assert CityTime().is_set() is False


def test_is_set_no_timezone():
    dt = CityTime()
    dt._datetime = datetime.datetime(2018, 1, 1, 10, 0)
    assert dt.is_set() is False


def test_check_set():
    with pytest.raises(ValueError):
        CityTime().check_set()


def test_check_set_no_timezone():
    dt = CityTime()
    dt._datetime = datetime.datetime(2018, 1, 1, 10, 0)
    with pytest.raises(ValueError):
        dt.check_set()


def test_bool():
    assert bool(CityTime()) is False


def test_bool_is_true():
    dt = CityTime(datetime.datetime(2018, 1, 1, 10, 0), 'US/Eastern')
    assert bool(dt) is True


@given(OneOfStrategy(strategies=(st.complex_numbers(), st.text(), st.binary())))
def test_increment_wrong_type(x):
    ct1 = CityTime(datetime.datetime(2018, 1, 1, 10, 0), 'US/Eastern')
    with pytest.raises((TypeError, ValueError)):
        ct1.increment(x)


def test_increment_no_data():
    dt = CityTime(datetime.datetime(2018, 1, 1, 10, 0), 'US/Eastern')
    with pytest.raises(ValueError):
        dt.increment()


def test_local_strftime():
    test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    test_time = CityTime(test_dt, 'UTC')
    assert test_time.local_strftime('%B') == test_dt.strftime('%B')


def test_local_strftime2():
    test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    test_time = CityTime(test_dt, 'UTC')
    assert test_time.local_strftime('%c') == test_dt.strftime('%c')


def test_utc_strftime():
    test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    test_time = CityTime(test_dt, 'UTC')
    assert test_time.utc_strftime('%B') == test_dt.strftime('%B')


def test_utc_strftime2():
    test_dt = datetime.datetime(2015, 7, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    test_time = CityTime(test_dt, 'UTC')
    assert test_time.utc_strftime('%c') == test_dt.strftime('%c')


def test_now():
    test_zone = ''
    callable_obj = getattr(CityTime, 'now')
    with pytest.raises(ValueError):
        callable_obj(test_zone)


def test_now2():
    callable_obj = getattr(CityTime, 'now')
    test_zone = 'Idontknow/WhereToGo'
    with pytest.raises(UnknownTimeZoneError):
        callable_obj(test_zone)


def test_utc():
    with pytest.raises(ValueError):
        CityTime().utc()


def test_local():
    with pytest.raises(ValueError):
        CityTime().local()


def test_local_minute():
    with pytest.raises(ValueError):
        CityTime().local_minute()


def test_timezone():
    with pytest.raises(ValueError):
        CityTime().timezone()


def test_tzinfo():
    with pytest.raises(ValueError):
        CityTime().tzinfo()


def test_weekday():
    with pytest.raises(ValueError):
        CityTime().weekday()


def test_day_name():
    with pytest.raises(ValueError):
        CityTime().day_name()


def test_day_abbr():
    with pytest.raises(ValueError):
        CityTime().day_abbr()


def test_time_string():
    with pytest.raises(ValueError):
        CityTime().time_string()


def test_increment():
    with pytest.raises(ValueError):
        CityTime().increment(days=1)


def test_increment2():
    with pytest.raises(ValueError):
        CityTime().increment(days=1)


def test_iso_format_bad_tz():
    ct = CityTime()
    with pytest.raises(UnknownTimeZoneError):
        ct.set_iso_format(EARLY_TIME.isoformat(), True)


def test_iso_format_bad_tz2():
    ct = CityTime()
    with pytest.raises(UnknownTimeZoneError):
        ct.set_iso_format(EARLY_TIME.isoformat(), "Mars")


def test_iso_format_bad_iso():
    ct = CityTime()
    with pytest.raises(AttributeError):
        ct.set_iso_format(True, "America/New_York")


def test_iso_format_bad_iso2():
    ct = CityTime()
    with pytest.raises(ValueError):
        ct.set_iso_format('2000-01-01T01:01:01+05:00', "America/New_York")


def test_epoch_not_set():
    with pytest.raises(ValueError):
        CityTime().epoch()
