__author__ = 'Thorsten'

import unittest
from CityTime import CityTime
from calendar import day_name
import datetime
import pytz
from pytz.exceptions import NonExistentTimeError


class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.early_time = datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)
        self.current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.utc = pytz.timezone('utc')
        self.eastern = pytz.timezone('US/Eastern')
        self.ct1 = CityTime()
        self.ct2 = CityTime()
        self.ct3 = CityTime()

    def test_initialization(self):
        self.assertRaises(ValueError, self.ct1.astimezone, 'utc')
        self.assertEqual(self.ct1._datetime, datetime.datetime.min)
        self.assertEqual(self.ct1._tz, pytz.timezone('UTC'))
        self.assertEqual(self.ct1._t_zone, '')
        self.ct2.set(self.current_time, 'US/Eastern')
        ct2 = CityTime(self.ct2)
        self.assertEqual(ct2._t_zone, 'US/Eastern')
        self.assertEqual(ct2._tz, pytz.timezone('US/Eastern'))
        self.assertEqual(ct2._datetime, self.current_time)

    def test__str__(self):
        ct1 = self.ct1
        self.assertEqual(ct1.__str__(), 'CityTime object not set yet.')
        ct1.set(self.current_time, 'US/Eastern')
        self.assertEqual(str(ct1), str(self.current_time))

    def test__eq__(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 == self.ct2)

    def test__ne__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 != self.ct2)

    def test__lt__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 < self.ct2)

    def test__le__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 <= self.ct2)
        self.ct1.set(self.current_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 <= self.ct2)

    def test__gt__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct2 > self.ct1)

    def test__ge__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct2 >= self.ct1)
        self.ct1.set(self.current_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertTrue(self.ct1 >= self.ct2)

    def test_set(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.assertEqual(self.ct1._datetime, self.current_time)
        self.assertEqual(self.ct1._tz, pytz.timezone('US/Eastern'))
        dt = datetime.datetime(year=2014, month=10, day=5, hour=10, minute=55, tzinfo=pytz.timezone('US/Central'))
        dt2 = dt.replace(hour=15, tzinfo=pytz.timezone('utc'))
        self.ct1.set(dt, 'US/Central')
        self.assertEqual(self.ct1._datetime, dt2)
        self.assertEqual(self.ct1._tz, pytz.timezone('US/Central'))

    def test_utc(self):
        self.ct1.set(self.current_time, 'utc')
        ct = self.current_time.replace(tzinfo=pytz.timezone('utc'))
        self.assertEqual(self.ct1.utc, ct)
        self.assertEqual(self.ct1.local.tzinfo, ct.tzinfo)

    def test_local(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        self.assertEqual(self.ct1.local, self.current_time)
        self.assertEqual(self.ct1.local.tzinfo, self.current_time.tzinfo)

    def test_astimezone(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        ct = self.current_time.astimezone(pytz.timezone('US/Central'))
        self.assertEqual(self.ct1.astimezone('US/Central'), ct)

    def test_local_minute(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        minutes = self.current_time.hour * 60 + self.current_time.minute
        self.assertEqual(self.ct1.local_minute, minutes)

    def test_timezone(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        self.assertEqual(self.ct1.timezone, str(self.current_time.tzinfo))

    def test_tzinfo(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        self.assertEqual(self.ct1.tzinfo, pytz.timezone(str(self.current_time.tzinfo)))

    def test_weekday(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        self.assertEqual(self.ct1.weekday, self.current_time.weekday())

    def test_day_name(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        name = day_name[self.current_time.weekday()]
        self.assertEqual(self.ct1.day_name, name)

    def test_day_abbr(self):
        weekdays = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        self.assertEqual(self.ct1.day_abbr, weekdays[self.current_time.weekday()])

    def test_time_string(self):
        self.ct1.set(self.current_time, str(self.current_time.tzinfo))
        time_string = self.current_time.strftime('%H%M')
        self.assertEqual(self.ct1.time_string, time_string)

    def test_increment(self):
        times = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
        # years and months aren't part of .increment() keyword arguments, so leave those out
        increments = times[2:6]
        # make a dict of the values of self.early_time
        t_args = dict(zip([x[:-1] for x in times], self.early_time.timetuple()))
        # then add the time zone
        t_args['tzinfo'] = pytz.timezone('Japan')
        # unpack the dict into the keyword arguments
        et = datetime.datetime(**t_args)
        # use it to set self.ct1, so that they're both the same
        self.ct1.set(et, 'Japan')
        for inc in increments:
            # increment each keyword argument by one (replace the 1 with a 2)
            et = et.replace(**{inc[:-1]: 2})
            # increment each keyword argument by one
            self.ct1.increment(**{inc: 1})
            self.assertEqual(self.ct1.local, et)


class NegativeTests(unittest.TestCase):

    def setUp(self):
        self.early_time = datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)
        self.current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.utc = pytz.timezone('utc')
        self.eastern = pytz.timezone('US/Eastern')
        self.ct1 = CityTime()
        self.ct2 = CityTime()
        self.ct3 = CityTime()

    def test_initialization(self):
        self.assertRaises(ValueError, self.ct1.astimezone, 'utc')
        self.assertRaises(TypeError, CityTime, 'int')
        self.assertRaises(TypeError, CityTime, 42)

    def test__eq__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertFalse(self.ct1 == self.ct2)
        self.assertFalse(self.ct1 == 2)

    def test__ne__(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        self.ct2.set(self.current_time, 'US/Eastern')
        self.assertFalse(self.ct1 != self.ct2)
        self.assertTrue(self.ct1 != 2)

    def test__lt__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1 < 2

    def test__le__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1 <= 2

    def test__gt__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1 > 2

    def test__ge__(self):
        self.ct1.set(self.early_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1 >= 2

    def test_set(self):
        with self.assertRaises(ValueError):
            self.ct1.set(2, 'US/Eastern')
        with self.assertRaises(ValueError):
            self.ct1.set(self.current_time, 2)
        with self.assertRaises(pytz.exceptions.UnknownTimeZoneError):
            self.ct1.set(self.current_time, 'US/Moscow')

    def test_check_set(self):
        self.assertRaises(ValueError, self.ct1.check_set)
        self.ct1._datetime = self.current_time
        self.assertRaises(ValueError, self.ct1.check_set)

    def test_increment(self):
        self.ct1.set(self.current_time, 'US/Eastern')
        with self.assertRaises(TypeError):
            self.ct1.increment('x')
        times = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
        # years and months aren't part of .increment() keyword arguments, so leave those out
        increments = times[2:6]
        # make a dict of the values of self.early_time
        t_args = dict(zip([x[:-1] for x in times], self.early_time.timetuple()))
        # then add the time zone
        t_args['tzinfo'] = pytz.timezone('Japan')
        # unpack the dict into the keyword arguments
        et = datetime.datetime(**t_args)
        # use it to set self.ct1, so that they're both the same
        self.ct1.set(et, 'Japan')
        for inc in increments:
            # increment each keyword argument by one (replace the 1 with a 2)
            et = et.replace(**{inc[:-1]: 2})
            # increment each keyword argument by one
            self.ct1.increment(**{inc: 1})
            self.assertEqual(self.ct1.local, et)

if __name__ == '__main__':
    unittest.main()
