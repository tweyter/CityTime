import unittest
from CityTime import CityTime
from calendar import day_name
import datetime
import pytz
from pytz.exceptions import NonExistentTimeError, AmbiguousTimeError
from pytz.exceptions import UnknownTimeZoneError
from hypothesis import given, assume
from hypothesis.specifiers import sampled_from, one_of
from hypothesis.extra.datetime import naive_datetime, timezone_aware_datetime


class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.datetime_min = datetime.datetime.min.replace(month=2)
        self.datetime_max = datetime.datetime.max.replace(day=1)
        self.max_td = self.datetime_max - self.datetime_min
        self.max_td_int = int(self.max_td.total_seconds())
        self.early_time = datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)
        self.current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.utc = pytz.timezone('utc')
        self.eastern = pytz.timezone('US/Eastern')
        self.ct1 = CityTime()
        self.ct2 = CityTime()
        self.ct3 = CityTime()
        self.sample_timezones = pytz.common_timezones_set

    def test_uninitialized(self):
        self.assertRaises(ValueError, self.ct1.astimezone, 'utc')

    def test_initialized_tz(self):
        self.assertEqual(self.ct1._tz, pytz.timezone('UTC'))

    def test_initialized_t_zone(self):
        self.assertEqual(self.ct1._t_zone, '')

    def test_set_t_zone(self):
        @given(datetime.datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            self.ct2.set(dt, tz)
            self.assertEqual(self.ct2._t_zone, tz)
        test_it()

    def test_set_tz(self):
        @given(datetime.datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            self.ct2.set(dt, tz)
            self.assertEqual(self.ct2._tz, pytz.timezone(tz))
        test_it()

    def test_set_datetime(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            dt1 = dt.replace(tzinfo=pytz.utc)
            ct1 = CityTime(dt1, tz)
            self.assertEqual(ct1._datetime.tzinfo, pytz.timezone('UTC'))
            self.assertEqual(ct1._datetime, dt1)
        test_it()

    def test_unset__str__(self):
        self.assertEqual(self.ct1.__str__(), 'CityTime object not set yet.')

    def test__str__(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, tz)
            dt_utc = dt.replace(tzinfo=pytz.utc)
            # slicing [:-6] removes the timezone offset
            self.assertEqual(str(ct1)[:-6], str(dt_utc)[:-6])
        test_it()

    def test__eq__(self):
        @given(datetime.datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, tz)
            ct2 = CityTime(dt, tz)
            self.assertEqual(ct1, ct2)
        test_it()

    def test__eq__to_datetime(self):
        @given(datetime.datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = self.ct1
            ct1.set(dt, tz)
            utc_time = self.ct1.utc()
            self.assertEqual(ct1, utc_time)
        test_it()

    def test__ne__(self):
        @given(naive_datetime, naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt1, dt2, tz):
            assume(dt1 != dt2)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt2, tz)
            self.assertNotEqual(ct1, ct2)
        test_it()

    def test__ne__non_datetime(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            assume(self.datetime_min < dt < self.datetime_max)
            ct1 = CityTime(dt, tz)
            non_datetime = {}
            self.assertNotEqual(ct1, non_datetime)
        test_it()

    def test__lt__(self):
        @given(naive_datetime, naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt1, dt2, tz):
            assume(dt2 < self.datetime_max)
            assume(dt1 > self.datetime_min)
            assume(dt1 < dt2)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt2, tz)
            self.assertLess(ct1, ct2)
        test_it()

    def test__le__(self):
        @given(naive_datetime, naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt1, dt2, tz):
            assume(dt2 < self.datetime_max)
            assume(dt1 > self.datetime_min)
            assume(dt1 <= dt2)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt2, tz)
            self.assertLessEqual(ct1, ct2)
        test_it()

    def test__gt__(self):
        @given(naive_datetime, naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt1, dt2, tz):
            assume(dt1 < self.datetime_max)
            assume(dt2 > self.datetime_min)
            assume(dt1 > dt2)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt2, tz)
            self.assertGreater(ct1, ct2)
        test_it()

    def test__ge__(self):
        @given(naive_datetime, naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt1, dt2, tz):
            assume(dt1 < self.datetime_max)
            assume(dt2 > self.datetime_min)
            assume(dt1 >= dt2)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt2, tz)
            self.assertGreaterEqual(ct1, ct2)
        test_it()

    def test__add__(self):
        @given(naive_datetime, int, sampled_from(self.sample_timezones))
        def test_it(dt1, i, tz):
            assume(-999999999 < i < 999999999)
            td = datetime.timedelta(seconds=i)
            if i > 0:
                assume(dt1 < self.datetime_max - td)
            elif i < 0:
                assume(dt1 > self.datetime_min - td)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt1, tz)
            ci = int(i)
            assert isinstance(ci, int)
            print(ci)
            ct2.increment(seconds=ci)
            self.assertEqual(ct1 + td, ct2)
            # check to see that ct1 is not changed, but that the method returned a new CityTime object
            self.assertFalse(ct1 is ct1 + td)
        test_it()

    def test__sub__(self):
        @given(naive_datetime, int, sampled_from(self.sample_timezones))
        def test_it(dt1, i, tz):
            assume(abs(i) < 999999999)
            td = datetime.timedelta(seconds=i)
            if i > 0:
                assume(dt1 < self.datetime_max - td)
            elif i < 0:
                assume(dt1 > self.datetime_min - td)
            ct1 = CityTime(dt1, tz)
            ct2 = CityTime(dt1, tz)
            ct2.increment(seconds=-i)
            self.assertEqual(ct1 - td, ct2)
            # check to see that ct1 is not changed, but that the method returned a new CityTime object
            self.assertFalse(ct1 is ct1 - td)
        test_it()

    def test__hash__(self):
        @given(datetime.datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, tz)
            self.assertEqual(ct1.__hash__(), ct1.utc().__hash__())
        test_it()

    def test_utc(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, 'utc')
            self.assertEqual(ct1.utc(), dt.replace(tzinfo=pytz.utc))
        test_it()

    def test_utc_tzinfo(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, 'utc')
            self.assertEqual(ct1.tzinfo(), pytz.utc)
        test_it()

    def test_local(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            self.assertEqual(ct1.local(), dt)
        test_it()

    def test_local_timezone(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            self.assertEqual(ct1.timezone(), str(dt.tzinfo))
        test_it()

    def test_astimezone(self):
        @given(timezone_aware_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            self.assertEqual(
                ct1.astimezone(tz),
                dt.astimezone(pytz.timezone(tz))
            )
        test_it()

    def test_local_minute(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            minutes = dt.hour * 60 + dt.minute
            self.assertEqual(ct1.local_minute(), minutes)
        test_it()

    def test_timezone(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, tz)
            self.assertEqual(ct1.timezone(), tz)
        test_it()

    def test_tzinfo(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            ct1 = CityTime(dt, tz)
            self.assertEqual(ct1.tzinfo(), pytz.timezone(tz))
        test_it()

    def test_weekday(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            self.assertEqual(ct1.weekday(), dt.weekday())
        test_it()

    def test_day_name(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            name = day_name[dt.weekday()]
            self.assertEqual(ct1.day_name(), name)
        test_it()

    def test_day_abbr(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            name = day_name[dt.weekday()]
            self.assertEqual(ct1.day_name(), name)
            self.assertEqual(ct1.day_abbr(), weekdays[dt.weekday()])
        test_it()

    def test_time_string(self):
        @given(timezone_aware_datetime)
        def test_it(dt):
            assume(str(dt.tzinfo) in self.sample_timezones)
            ct1 = CityTime(dt, str(dt.tzinfo))
            time_string = dt.strftime('%H%M')
            self.assertEqual(ct1.time_string(), time_string)
        test_it()

    def test_increment(self):
        @given(naive_datetime, sampled_from(self.sample_timezones), int, int, int, int)
        def test_it(dt, tz, d, h, m, s):
            assume(abs(d) < 99999)
            assume(abs(h) < 9999999)
            assume(abs(m) < 999999999)
            assume(abs(s) < 999999999)
            td = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
            if td > datetime.timedelta():
                assume(dt < self.datetime_max - td)
            elif td < datetime.timedelta():
                assume(dt > self.datetime_min - td)
            ct1 = CityTime(dt, tz)
            ct2 = CityTime(dt, tz)
            ct1.increment(days=d, hours=h, minutes=m, seconds=s)
            if td == datetime.timedelta():
                self.assertEqual(ct1, ct2)
            else:
                self.assertNotEqual(ct1, ct2)
        test_it()

    def test_local_strftime(self):
        formats = ('%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X')
        test_time = self.ct1
        test_time.set(self.current_time, str(self.current_time.tzinfo))
        for form in formats:
            self.assertEqual(test_time.local_strftime(form), self.current_time.strftime(form))

    def test_utc_strftime(self):
        formats = ('%a', '%A', '%w', '%d', '%b', '%B', '%c', '%x', '%X')
        test_time = self.ct1
        test_time.set(self.current_time, str(self.current_time.tzinfo))
        test_utc = test_time.utc()
        for form in formats:
            self.assertEqual(test_time.utc_strftime(form), test_utc.strftime(form))

    def test_today(self):
        test_time = CityTime.today()
        self.assertIsInstance(test_time, CityTime)
        self.assertIsInstance(test_time.local(), datetime.datetime)
        self.assertEqual(test_time.timezone(), 'UTC')
        test_date = datetime.date.today()
        self.assertEqual(test_time.local().date(), test_date)

    def test_now(self):
        test_zone = 'America/Chicago'
        test_time = CityTime.now(test_zone)
        test_date = datetime.date.today()
        self.assertIsInstance(test_time, CityTime)
        self.assertEqual(test_time.timezone(), test_zone)
        self.assertEqual(test_time.local().date(), test_date)


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

    def test_initialization(self):
        self.assertRaises(ValueError, self.ct1.astimezone, 'utc')
        self.assertRaises(TypeError, CityTime, 'int')
        self.assertRaises(TypeError, CityTime, 42)

    def test__eq__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct1.check_set()
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertNotEqual(self.ct1, self.ct2)
        self.assertNotEqual(self.ct1, 2)
        self.assertNotEqual(self.ct1, 'X')
        utc_time = self.ct1.utc().replace(year=2013)
        self.assertNotEqual(self.ct1, utc_time)
        non_datetime = {}
        self.assertNotEqual(self.ct1, non_datetime)

    def test__ne__false(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertFalse(self.ct1 != self.ct2)

    def test__ne__true(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            ct1 = CityTime(self.early_time, 'US/Eastern')
            self.assertNotEqual(ct1, x)
        test_it()

    def test__ne__datetime(self):
        @given(naive_datetime, sampled_from(self.sample_timezones))
        def test_it(dt, tz):
            assume(dt.minute != 1)
            dt1 = dt.replace(tzinfo=pytz.utc)
            ct1 = CityTime(dt1.replace(minute=1), tz)
            self.assertNotEqual(ct1, dt1)
        test_it()

    def test__lt__(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(TypeError):
                self.ct1 < x
        test_it()

    def test__le__(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(TypeError):
                self.ct1 <= x
        test_it()

    def test__gt__(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(TypeError):
                self.ct1 > x
        test_it()

    def test__ge__(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(TypeError):
                self.ct1 >= x
        test_it()

    def test_set_dt(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises((AttributeError, TypeError)):
                self.ct1.set(x, 'US/Eastern')
        test_it()

    def test_set_tz(self):
        @given(one_of((int, bool, None, float, complex, str, bytes)))
        def test_it(x):
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(UnknownTimeZoneError):
                self.ct1.set(self.current_time, x)
        test_it()

    def test_set_unknown_tz(self):
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            self.ct1.set(self.current_time, 'US/Moscow')

    def test_set_date_instead_of_datetime(self):
        @given(int)
        def test_it(y):
            assume(0 < y < 9999)
            date = datetime.date(y, 1, 1)
            self.ct1.set(self.early_time, 'US/Eastern')
            with self.assertRaises(TypeError):
                self.ct1.set(date, 'US/Eastern')
        test_it()

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

    def test_increment_wrong_type(self):
        @given(one_of((bool, None, float, complex, str, bytes)))
        def test_it(x):
            ct1 = CityTime(self.current_time, 'US/Eastern')
            with self.assertRaises((TypeError, ValueError)):
                ct1.increment(x)
        test_it()

    def test_increment_no_data(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.assertRaises(ValueError, self.ct1.increment)

    def test_increment_non_existant_time(self):
        # See notes in CityTime.increment
        pass

    def test_local_strftime(self):
        formats = ('%+', '%[')
        test_time = self.ct1
        test_time.set(self.current_time, str(self.current_time.tzinfo))
        for form in formats:
            self.assertEqual(test_time.local_strftime(form), None)

    def test_utc_strftime(self):
        formats = ('%+', '%[')
        test_time = self.ct1
        test_time.set(self.current_time, str(self.current_time.tzinfo))
        test_utc = test_time.utc()
        for form in formats:
            self.assertEqual(test_time.utc_strftime(form), None)

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

if __name__ == '__main__':
    unittest.main()
