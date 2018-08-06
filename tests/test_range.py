import datetime

import hypothesis.strategies as st
import pytz
from hypothesis import given, assume
from hypothesis.strategies import datetimes
import pytest

from citytime import CityTime, Range

TIMEZONES = pytz.common_timezones

START_TIME = CityTime(datetime.datetime(2015, 12, 31, 23, 59), 'UTC')
END_TIME = CityTime(datetime.datetime(2016, 1, 1, 0, 1), 'UTC')


def test_empty_init():
    r = Range()
    assert r._members == set()


def test_full_init():
    r = Range(START_TIME, END_TIME)
    assert r._members != set()


def test_wrong_init():
    ve = 'Range object requires two parameters, either <CityTime, CityTime> or <CityTime, datetime.timedelta>'
    with pytest.raises(ValueError) as cm:
        Range(2)
    assert ve == str(cm.value)


def test_create_range():
    r = Range()
    r._create_range(START_TIME, END_TIME)
    assert r._members == {START_TIME, END_TIME}


def test_create_range_not_city_time():
    r = Range()
    with pytest.raises(ValueError):
        r._create_range(START_TIME, 2)


def test_create_range_city_time_not_set():
    r = Range()
    with pytest.raises(ValueError):
        r._create_range(START_TIME, CityTime())


def test_start_time():
    r = Range(END_TIME, START_TIME)  # purposely reversing the order
    assert r.start_time() == START_TIME


def test_end_time():
    r = Range(END_TIME, START_TIME)  # purposely reversing the order
    assert r.end_time() == END_TIME


def test_create_range_timedelta():
    r = Range()
    r._create_range_timedelta(START_TIME, datetime.timedelta(minutes=1))
    check = map(lambda x: isinstance(x, CityTime), r._members)
    assert all(check) is True


def test_create_range_timedelta_using_init():
    r = Range(START_TIME, datetime.timedelta(minutes=1))
    check = map(lambda x: isinstance(x, CityTime), r._members)
    assert all(check) is True


def test_create_range_bad_data():
    r = Range()
    with pytest.raises(ValueError):
        r._create_range_timedelta(2, datetime.timedelta())
    with pytest.raises(ValueError):
        r._create_range_timedelta(CityTime(), datetime.timedelta())
    with pytest.raises(ValueError):
        r._create_range_timedelta(START_TIME, 2)


def test_check_set():
    r = Range(START_TIME, END_TIME)
    assert r.check_set() is True


def test_check_set_false():
    r = Range()
    assert r.check_set() is False


def test_delta():
    """
    Test for the delta method which calculates the timedelta between start time and
    end time.

    start_time and end_time must be set to CityTime objects, and each
    CityTime object must be set to a valid time.

    The method should return a valid datetime.timedelta.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    assert r.delta() == END_TIME - START_TIME


def test_delta_not_set():
    r = Range()
    assert r.delta() == datetime.timedelta()


def test_contains_range():
    """
    Test for the contains method which determines if the start and end times of
    one Range object fall entirely within the start and end times of another
    Range object.

    Assumes that both Range objects are set with valid CityTimes.
    The contains method should return a boolean.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    contained = Range(START_TIME, END_TIME)
    assert r.contains(contained) is True


def test_contains_citytime():
    """
    Test for the contains method to see that it can also test for
    an individual CityTime object to be contained within the range.
    @return:
    """

    r = Range(START_TIME, END_TIME)
    contained = START_TIME
    assert r.contains(contained) is True


def test_contains_false():
    r = Range(START_TIME, END_TIME)
    not_contained = Range(END_TIME, datetime.timedelta(hours=-1))
    assert r.contains(not_contained) is False


def test_contains_errors():
    r = Range()
    with pytest.raises(ValueError) as cm:
        r.contains(START_TIME)
    assert 'Range is not set.' == str(cm.value)


def test_contains_errors2():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.contains(Range())
    assert 'Object to be compared is not set.' == str(cm.value)


def test_contains_none():
    r = Range(START_TIME, END_TIME)
    assert r.contains(None) is False


def test_contains_outside_of_range():
    r = Range(START_TIME, END_TIME)
    t = START_TIME.copy()
    t.increment(days=-1)
    assert r.contains(t) is False


def test_overlaps():
    """
    Test for the overlaps method which determines if either the start time
    or end time of another Range object falls within the range of the current
    Range object.

    Assumes that both Range objects are set with valid CityTimes.
    The overlaps method should return a boolean.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    overlap_range = Range(START_TIME, datetime.timedelta(days=100))
    assert r.overlaps(overlap_range) is True


def test_overlaps_start_time():
    """
    Similar test to test_overlaps, but this time we overlap the start time instead
    of the end time.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    overlap_range = Range(END_TIME, datetime.timedelta(days=-100))
    assert r.overlaps(overlap_range) is True


def test_overlaps_with_contained_range():
    """
    Another test of the overlaps method, but with a range that is entirely
    contained within the Range object.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    overlap_range = Range(START_TIME, END_TIME)
    assert r.overlaps(overlap_range) is True


def test_overlaps_false():
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(days=-1)
    non_overlap = Range(new_start_time, datetime.timedelta(hours=1))
    assert r.overlaps(non_overlap) is False


def test_overlaps_wrong_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError) as cm:
        r.overlaps(True)
    assert str(cm.value) == "Object to be compared must be of type 'Range'"


def test_overlaps_not_set():
    r = Range()
    cr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.overlaps(cr)
    assert str(cm.value) == 'Range is not set.'


def test_overlaps_param_not_set():
    cr = Range()
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.overlaps(cr)
    assert str(cm.value) == 'Range object to be compared is not set.'


def test_overlaps_param_is_none():
    r = Range(START_TIME, END_TIME)
    assert r.overlaps(None) is False


def test_overlap():
    """
    Test for the overlap method, which determines how much of one Range object
    overlaps with another Range object.

    Assumes that both Range objects are set with valid CityTimes.
    The overlap method should return a datetime.timedelta.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    overlap_range = Range(START_TIME, datetime.timedelta(days=100))
    assert r.overlap(overlap_range) == r.delta()


def test_overlap_start_time():
    """
    Similar to test_overlap, but tests a trip that overlaps the start_time
    of the base Range object.

    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(hours=-100)
    overlap_range = Range(new_start_time, END_TIME)
    assert r.overlap(overlap_range) == r.delta()


def test_not_overlapping():
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(days=-1)
    non_overlap = Range(new_start_time, datetime.timedelta(hours=1))
    assert r.overlap(non_overlap) == datetime.timedelta()


def test_overlap_not_set():
    r = Range()
    cr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.overlap(cr)
    assert str(cm.value) == 'Range is not set.'


def test_overlap_param_not_set():
    cr = Range()
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.overlap(cr)
    assert str(cm.value) == 'Range object to be compared is not set.'


def test_same_as():
    """
    Test of equality that returns True if both start times and end times are
    equal to each other.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    equals = Range(START_TIME, END_TIME)
    assert r == equals


def test_not_same():
    """
    Test of inequality between Range objects.

    Returns True if either the start_times don't match or the end_times don't match.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=1)
    equals = Range(new_start_time, END_TIME)
    assert r != equals


def test_before():
    r = Range(START_TIME, END_TIME)
    new_end_time = END_TIME.copy()
    new_end_time.increment(hours=-1)
    lesser = Range(new_end_time, new_end_time)
    assert lesser.before(r) is True


def test_before_wrong_type():
    r = Range(START_TIME, END_TIME)
    result = r.before(2)
    assert NotImplemented == result


def test_before_not_set():
    r = Range()
    cr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.before(cr)
    assert str(cm.value) == 'Range is not set.'


def test_before_param_not_set():
    cr = Range()
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.before(cr)
    assert str(cm.value) == 'Range object to be compared is not set.'


def test_after():
    r = Range(START_TIME, END_TIME)
    new_end_time = END_TIME.copy()
    new_end_time.increment(hours=-1)
    lesser = Range(new_end_time, new_end_time)
    assert r.after(lesser) is True


def test_after_wrong_type():
    r = Range(START_TIME, END_TIME)
    result = r.after(2)
    assert NotImplemented == result


def test_after_not_set():
    r = Range()
    cr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.after(cr)
    assert str(cm.value) == 'Range is not set.'


def test_after_param_not_set():
    cr = Range()
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        r.after(cr)
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__eq__():
    r = Range(START_TIME, END_TIME)
    s = Range(START_TIME, END_TIME)
    assert r == s


def test__eq__not_range():
    r = Range(START_TIME, END_TIME)
    assert (r == 3) is False


def test__eq__not_set():
    r = Range()
    s = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r == s
    assert str(cm.value) == 'Range is not set.'


def test__eq__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r == Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__eq__false():
    r = Range(START_TIME, END_TIME)
    cr = r.copy()
    cr.extend_prior(datetime.timedelta(seconds=1))
    assert (r == cr) is False


def test__ne__():
    r = Range(START_TIME, END_TIME)
    s = r.copy()
    s.extend(datetime.timedelta(seconds=1))
    assert r != s


def test__ne__not_range():
    r = Range(START_TIME, END_TIME)
    result = r != 3
    assert result is True


def test__ne__not_set():
    r = Range()
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r != r
    assert str(cm.value) == 'Range is not set.'


def test__ne__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r != Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__ne__false():
    r = Range(START_TIME, END_TIME)
    result = r != r
    assert result is False


def test__lt__():
    r = Range(START_TIME, END_TIME)
    s = r.copy()
    s.extend(datetime.timedelta(seconds=1))
    assert r < s


def test__lt__not_range():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError) as cm:
        # noinspection PyStatementEffect
        r < 3
    assert str(cm.value) == "unorderable types: Range, <class 'int'>"


def test__lt__not_set():
    r = Range()
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r < r
    assert str(cm.value) == 'Range is not set.'


def test__lt__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r < Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__lt__false():
    r = Range(START_TIME, END_TIME)
    result = r < r
    assert result is False


def test__le__():
    r = Range(START_TIME, END_TIME)
    s = r.copy()
    assert r <= s
    s.extend(datetime.timedelta(seconds=1))
    assert r <= s


def test__le__not_range():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError) as cm:
        # noinspection PyStatementEffect
        r <= 3
    assert str(cm.value) == "unorderable types: Range, <class 'int'>"


def test__le__not_set():
    r = Range()
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r <= r
    assert str(cm.value) == 'Range is not set.'


def test__le__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r <= Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__le__false():
    r = Range(START_TIME, END_TIME)
    cr = r.copy()
    r.extend(datetime.timedelta(seconds=1))
    result = r <= cr
    assert result is False


def test__gt__():
    r = Range(START_TIME, END_TIME)
    s = r.copy()
    s.extend(datetime.timedelta(seconds=1))
    assert s > r


def test__gt__not_range():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError) as cm:
        # noinspection PyStatementEffect
        r > 3
    assert str(cm.value) == "unorderable types: Range, <class 'int'>"


def test__gt__not_set():
    r = Range()
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r > r
    assert str(cm.value) == 'Range is not set.'


def test__gt__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r > Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__gt__false():
    r = Range(START_TIME, END_TIME)
    result = r > r
    assert result is False


def test__ge__():
    r = Range(START_TIME, END_TIME)
    s = r.copy()
    assert s >= r
    s.extend(datetime.timedelta(seconds=1))
    assert s >= r


def test__ge__not_range():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError) as cm:
        # noinspection PyStatementEffect
        r >= 3
    assert str(cm.value) == "unorderable types: Range, <class 'int'>"


def test__ge__not_set():
    r = Range()
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r >= r
    assert str(cm.value) == 'Range is not set.'


def test__ge__other_not_set():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError) as cm:
        # noinspection PyStatementEffect
        r >= Range()
    assert str(cm.value) == 'Range object to be compared is not set.'


def test__ge__false():
    r = Range(START_TIME, END_TIME)
    cr = r.copy()
    r.extend(datetime.timedelta(seconds=1))
    result = cr >= r
    assert result is False


def test__str__():
    r = Range(START_TIME, END_TIME)
    assert r.__str__() == "Range: start: {} - end: {}".format(START_TIME.__str__(), END_TIME.__str__())


def test__repr__():
    r = Range(START_TIME, END_TIME)
    assert r.__repr__() == "Range: start: {} - end: {}".format(START_TIME.__str__(), END_TIME.__str__())


def test__bool__():
    r = Range()
    assert bool(r) is False


def test_extend():
    """
    Test for the extend method, which extends (ie. sets to a later time)
    the end_time of the Range object by the given timedelta.

    Assumes that the argument is a datetime.timedelta and that its value is positive.
    Assumes that the Range object is set.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    delta = r.delta()
    extension = datetime.timedelta(days=1)
    r.extend(extension)
    assert r.delta() == delta + extension


def test_extend_wrong_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError):
        r.extend(2)


def test_extend_negative_delta():
    r = Range(START_TIME, END_TIME)
    delta = datetime.timedelta(days=-1)
    with pytest.raises(ValueError):
        r.extend(delta)


def test_extend_not_set():
    r = Range()
    delta = datetime.timedelta(days=-1)
    with pytest.raises(ValueError):
        r.extend(delta)


def test_extend_prior():
    """
    Test for the extend_prior method, which extends (ie. sets to an earlier time)
    the start_time of the Range object by the given timedelta.

    Assumes that the argument is a datetime.timedelta and that its value is positive.
    Assumes that the Range object is set.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    delta = r.delta()
    extension = datetime.timedelta(days=1)
    r.extend_prior(extension)
    assert r.delta() == delta + extension


def test_extend_prior_wrong_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError):
        r.extend_prior(2)


def test_extend_prior_negative_delta():
    r = Range(START_TIME, END_TIME)
    delta = datetime.timedelta(days=-1)
    with pytest.raises(ValueError):
        r.extend_prior(delta)


def test_extend_prior_not_set():
    r = Range()
    delta = datetime.timedelta(days=-1)
    with pytest.raises(ValueError):
        r.extend_prior(delta)


def test_replace_start_time():
    """
    Test for the replace_start_time method, which alters the current Range object
    by assigning it a new start_time value.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=1)
    r.replace_start_time(new_start_time)
    assert r == Range(new_start_time, END_TIME)


def test_replace_start_time_wrong_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError):
        r.replace_start_time(2)


def test_replace_start_time_not_set():
    r = Range()
    with pytest.raises(ValueError):
        r.replace_start_time(START_TIME)


def test_replace_end_time():
    """
    Test for the replace_end_time method, which alters the current Range object
    by assigning it a new end_time value.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_end_time = END_TIME.copy()
    new_end_time.increment(minutes=1)
    r.replace_end_time(new_end_time)
    assert r == Range(START_TIME, new_end_time)


def test_replace_end_time_end_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError):
        r.replace_end_time(2)


def test_replace_end_time_not_set():
    r = Range()
    with pytest.raises(ValueError):
        r.replace_end_time(START_TIME)


def test_intersection():
    """
    Test for the intersection method, which creates a new Range object out of the
    where the two Range objects overlap.

    Assumes that both Range objects are set with valid CityTimes.
    The intersection method should return a new Range object.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = END_TIME.copy()
    new_start_time.increment(minutes=-1)
    new_end_time = END_TIME.copy()
    new_end_time.increment(minutes=1)
    intersector = Range(new_start_time, new_end_time)
    assert r.intersection(intersector) == Range(new_start_time, END_TIME)


def test_intersection_contained():
    """
    Test for a range that is smaller than, and entirely contained within,
    the current object.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME
    new_start_time.increment(minutes=1)
    new_end_time = END_TIME
    new_end_time.increment(minutes=-1)
    contained = Range(new_start_time, new_end_time)
    assert r.intersection(contained) == contained


def test_intersection__gt__():
    """
    Test to see that a Range object that is entirely outside of (greater than)
    the current object returns a value of None.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = END_TIME.copy()
    new_start_time.increment(minutes=1)
    greater = Range(new_start_time, new_start_time)
    assert r.intersection(greater) == Range()


def test_intersection__lt__():
    """
    Test to see that a Range object that is entirely outside of (less than)
    the current object returns a value of None.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=-1)
    lesser = Range(new_start_time, new_start_time)
    assert r.intersection(lesser) == Range()


def test_intersection_not_set():
    r = Range()
    nr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError):
        r.intersection(nr)


def test_intersection_other_not_set():
    r = Range()
    nr = Range(START_TIME, END_TIME)
    with pytest.raises(ValueError):
        nr.intersection(r)


def test_intersection_contained_in_other():
    """
    Test for the intersection method, when the Range object is contained entirely
    within the Range object given in the parameter.

    @return:
    """
    r = Range(START_TIME, END_TIME)
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=-1)
    new_end_time = END_TIME.copy()
    new_end_time.increment(minutes=1)
    intersector = Range(new_start_time, new_end_time)
    assert r.intersection(intersector) == r


def test_intersection_overlaps_start_time():
    new_end_time = END_TIME.copy()
    new_end_time.increment(minutes=1)
    r = Range(START_TIME, new_end_time)
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=-1)
    intersector = Range(new_start_time, END_TIME)
    assert r.intersection(intersector) == Range(START_TIME, END_TIME)


def test_intersection_overlaps_end_time():
    new_start_time = START_TIME.copy()
    new_start_time.increment(minutes=-1)
    r = Range(new_start_time, END_TIME)
    new_end_time = END_TIME.copy()
    new_end_time.increment(minutes=1)
    intersector = Range(START_TIME, new_end_time)
    assert r.intersection(intersector) == Range(START_TIME, END_TIME)


def test_copy():
    """
    Test of the copy method, which returns a deep copy of the Range instance.
    @return:
    """
    r = Range(START_TIME, END_TIME)
    copied = r.copy()

    # Check to see that the two objects have the same value
    assert r == copied

    # Check to see that they are unique objects.
    assert id(r) != id(copied)

    # Check to see that the start_times are unique objects
    assert id(r.start_time()) != id(copied.start_time())

    # Check to see that the end_times are unique objects
    assert id(r.end_time()) != id(copied.end_time())


def test_copy_not_set():
    r = Range()
    with pytest.raises(ValueError):
        r.copy()


def test_shift():
    r = Range(START_TIME, END_TIME)
    start_check = START_TIME.copy()
    start_check.increment(days=1)
    end_check = END_TIME.copy()
    end_check.increment(days=1)
    r.shift(datetime.timedelta(days=1))
    assert r.start_time() == start_check
    assert r.end_time() == end_check


def test_shift_wrong_type():
    r = Range(START_TIME, END_TIME)
    with pytest.raises(TypeError):
        r.shift(2)


"""
Hypothesis based tests
"""


@given(datetimes(timezones=st.none()), datetimes(timezones=st.none()))
def test__init__(dt, dt2):
    assume(dt <= dt2)
    start_time = CityTime(dt, 'UTC')
    end_time = CityTime(dt2, 'UTC')
    r1 = Range(start_time, end_time)
    assert r1._members == {start_time, end_time}


@given(datetimes(timezones=st.none()), st.integers())
def test__init__timedelta(dt, delta):
    assume(overflow(dt, delta))
    start_time = CityTime(dt, 'UTC')
    td = datetime.timedelta(seconds=delta)
    end_time = CityTime(dt, 'UTC')
    end_time.increment(seconds=delta)
    r = Range(start_time, td)
    assert r._members == {start_time, end_time}


@given(datetimes(timezones=st.none()), datetimes(timezones=st.none()))
def test_start_time(start, end):
    assume(start <= end)
    start_time = CityTime(start, 'UTC')
    r = Range(start_time, CityTime(end, 'UTC'))
    assert start_time == r.start_time()


@given(datetimes(timezones=st.none()), datetimes(timezones=st.none()))
def test_end_time(start, end):
    assume(start <= end)
    end_time = CityTime(start, 'UTC')
    r = Range(CityTime(end, 'UTC'), end_time)
    assert end_time == r.start_time()


@given(datetimes(timezones=st.none()), st.integers())
def test_delta(dt, delta):
    assume(overflow(dt.replace(microsecond=0), delta))
    start_time = CityTime(dt.replace(microsecond=0), 'UTC')
    td = datetime.timedelta(seconds=delta)
    r = Range(start_time, td)
    if delta >= 0:
        assert r.delta() == td
    else:
        assert r.delta() == -td


@given(datetimes(timezones=st.none()), st.integers(min_value=0), st.integers(min_value=0))
def test_contains(dt, delta1, delta2):
    time = dt.replace(microsecond=0)
    assume(overflow(time, delta1))
    assume(delta2 <= delta1)
    start_time = CityTime(time, 'UTC')
    td1 = datetime.timedelta(seconds=delta1)
    td2 = datetime.timedelta(seconds=delta2)
    r1 = Range(start_time, td1)
    end_time = r1.end_time()
    r2 = Range(start_time, td2)
    with pytest.raises(TypeError):
        r1.contains(str())
    if delta1 == delta2:
        assert r1.contains(r2) is True
        assert r2.contains(r1) is True
        return
    assert r1.contains(r2) is True
    assert r2.contains(r1) is False
    r3 = Range(end_time, -td2)
    assert r1.contains(r3) is True
    assert r3.contains(r1) is False


@given(datetimes(timezones=st.none()), st.integers(min_value=0), st.integers(min_value=0))
def test_overlaps(dt, delta1, delta2):
    time = dt.replace(microsecond=0)
    assume(overflow(time, delta1))
    assume(overflow(time, delta1 - delta2))
    start_time = CityTime(time, 'UTC')
    td1 = datetime.timedelta(seconds=delta1)
    td2 = datetime.timedelta(seconds=delta2)
    r1 = Range(start_time, td1)
    r2 = Range(start_time, td2)
    assert r1.overlaps(r2) is True
    assert r2.overlaps(r1) is True


@given(datetimes(timezones=st.none()), st.integers(min_value=0), st.integers(min_value=0))
def test_overlaps2(dt, delta1, delta2):
    time = dt.replace(microsecond=0)
    assume(overflow(time, delta1))
    assume(overflow(time, delta1 - delta2))
    start_time = CityTime(time, 'UTC')
    td1 = datetime.timedelta(seconds=delta1)
    td2 = datetime.timedelta(seconds=delta2)
    r1 = Range(start_time, td1)
    end_time = r1.end_time()
    r3 = Range(end_time, -td2)
    assert r1.overlaps(r3) is True
    assert r3.overlaps(r1) is True


@given(
    datetimes(timezones=st.none()),
    datetimes(timezones=st.none()),
    st.integers(min_value=0),
    st.integers(max_value=0)
)
def test_overlaps_false(dt1, dt2, delta1, delta2):
    assume(dt1 > dt2)
    assume(overflow(dt1, delta1))
    assume(overflow(dt2, delta2))
    r1 = Range(CityTime(dt1, 'UTC'), datetime.timedelta(seconds=delta1))
    r2 = Range(CityTime(dt2, 'UTC'), datetime.timedelta(seconds=delta2))
    assert r1.overlaps(None) is False
    assert r1.overlaps(r2) is False
    assert r2.overlaps(r1) is False


@given(datetimes(timezones=st.none()), st.integers(min_value=0), st.integers(min_value=0))
def test_overlap(dt, delta1, delta2):
    time = dt.replace(microsecond=0)
    assume(overflow(time, delta1))
    assume(delta2 < delta1)
    start_time = CityTime(time, 'UTC')
    td1 = datetime.timedelta(seconds=delta1)
    td2 = datetime.timedelta(seconds=delta2)
    r1 = Range(start_time, td1)
    end_time = r1.end_time()
    r2 = Range(start_time, td2)
    assert r2.delta() == r1.overlap(r2)
    assert r2.delta() == r1.overlap(r2)
    r3 = Range(end_time, -td2)
    assert r2.delta() == r1.overlap(r3)
    assert r2.delta() == r3.overlap(r1)


@given(st.integers(min_value=0))
def test_timedelta_to_h_mm(d):
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
