"""
Unit tests ConvertDatetimeValue methods
"""
import numpy as np

from gnome.basic_types import (ts_format,
                               datetime_value_1d,
                               datetime_value_2d,
                               time_value_pair)

from gnome.utilities.convert import (to_time_value_pair,
                                     to_datetime_value_1d,
                                     to_datetime_value_2d,
                                     tsformat)
from gnome.utilities.time_utils import (zero_time,
                                        sec_to_date)

import pytest


@pytest.fixture(scope='module')
def wind_ts(rq_wind):
    """
    setup a wind timeseries - uses the rq_wind fixture to get the
    wind values used for conversions
    - returns a dict with the expected datetime_rq, datetime_uv
      and time_value_pair objects
    """
    date_times = ([sec_to_date(zero_time())] * len(rq_wind['rq']))
    dtv_rq = (np.array(zip(date_times, rq_wind['rq']), dtype=datetime_value_2d)
              .view(dtype=np.recarray))

    date_times = ([sec_to_date(zero_time())] * len(rq_wind['uv']))
    dtv_uv = (np.array(zip(date_times, rq_wind['uv']), dtype=datetime_value_2d)
              .view(dtype=np.recarray))

    date_times = ([zero_time()] * len(rq_wind['uv']))
    tv = (np.array(zip(date_times, rq_wind['uv']), dtype=time_value_pair)
          .view(dtype=np.recarray))

    print 'Test Case - actual values:'
    print 'datetime_value_2d: datetime, (r, theta):'
    print dtv_rq.time
    print dtv_rq.value

    print '----------'
    print 'datetime_value_2d: datetime, (u, v):'
    print dtv_uv.time
    print dtv_uv.value

    print '----------'
    print 'time_value_pair: time, (u, v):'
    print tv.time
    print tv.value.reshape(len(tv.value), -1)

    return {'dtv_rq': dtv_rq, 'dtv_uv': dtv_uv, 'tv': tv}


def test_exceptions(wind_ts, invalid_rq):
    """
    test exceptions
    """
    with pytest.raises(ValueError):
        # incorrect dtype
        to_time_value_pair(wind_ts['tv'], ts_format.magnitude_direction)

    with pytest.raises(ValueError):
        # incorrect format
        to_time_value_pair(wind_ts['dtv_rq'], -1)
        to_datetime_value_2d(wind_ts['tv'], -1)

    with pytest.raises(ValueError):
        # string input can only be 'r-theta' or 'uv'
        to_time_value_pair(wind_ts['dtv_rq'], 'magnitude')
        to_datetime_value_2d(wind_ts['tv'], 'magnitude')

    # following also raises ValueError. This gives invalid (r,theta) inputs
    # which are rejected by the transforms.r_theta_to_uv_wind method.
    # It tests the inner exception is correct
    with pytest.raises(ValueError):
        length_of_dim1 = len(invalid_rq['rq'])
        zero_times = [zero_time()] * length_of_dim1

        invalid_dtv_rq = np.array(zip(zero_times, invalid_rq['rq']),
                                  dtype=datetime_value_2d)

        invalid_dtv_rq['value'] = invalid_rq['rq']

        to_time_value_pair(invalid_dtv_rq, ts_format.magnitude_direction)


@pytest.mark.parametrize("format_", ['uv', 'r-theta', 'r_theta'])
def test_ts_format(format_):
    if format_ == 'uv':
        assert tsformat(format_) == ts_format.uv
    else:
        assert tsformat(format_) == ts_format.r_theta

# tolerance for numpy.allclose(...)

atol = 1e-14
rtol = 0


@pytest.mark.parametrize('in_ts_format',
                         [ts_format.magnitude_direction, 'r-theta'])
def test_to_time_value_pair(wind_ts, in_ts_format):
    out_tv = (to_time_value_pair(wind_ts['dtv_rq'], in_ts_format)
              .view(dtype=np.recarray))

    # assert np.all(wind_ts['tv'].time == out_tv.time)
    assert np.allclose(wind_ts['tv'].value.u, out_tv.value.u, atol, rtol)
    assert np.allclose(wind_ts['tv'].value.v, out_tv.value.v, atol, rtol)


def test_to_time_value_pair_from_1d():
    length_of_dim1 = 4
    zero_times = [sec_to_date(zero_time())] * length_of_dim1
    rand_data = np.random.uniform(1, 10, length_of_dim1)

    data = np.array(zip(zero_times, rand_data), dtype=datetime_value_1d)
    out_tv = to_time_value_pair(data)

    assert np.all(out_tv['value']['v'] == 0.0)
    assert np.all(out_tv['value']['u'] == data['value'])


def test_to_datetime_value_1d(wind_ts):
    'test convert from time_value_pair to datetime_value_1d'
    out_dtval = to_datetime_value_1d(wind_ts['tv']).view(dtype=np.recarray)

    assert len(out_dtval.shape) == 1
    assert np.all(out_dtval['value'] == wind_ts['tv'].value.u)


@pytest.mark.parametrize('out_ts_format',
                         [ts_format.magnitude_direction, 'r-theta'])
def test_to_datetime_value_2d_rq(wind_ts, out_ts_format):
    out_dtval = (to_datetime_value_2d(wind_ts['tv'], out_ts_format)
                 .view(dtype=np.recarray))

    assert np.all(out_dtval.time == wind_ts['dtv_rq'].time)
    assert np.allclose(out_dtval.value, wind_ts['dtv_rq'].value, atol, rtol)


@pytest.mark.parametrize('out_ts_format', [ts_format.uv, 'uv'])
def test_to_datetime_value_2d_uv(wind_ts, out_ts_format):
    out_dtval = (to_datetime_value_2d(wind_ts['tv'], out_ts_format)
                 .view(dtype=np.recarray))

    assert np.allclose(out_dtval.value, wind_ts['dtv_uv'].value, atol, rtol)
