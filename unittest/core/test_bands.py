from __future__ import division

import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import pytest

from acoustics.core.bands import (octave, octave_high, octave_low, third,
                                  third_low, third_high, third2oct,
                                  _check_band_type)


def setup_module(bands):
    bands.octave_real = np.array([16,   31.5,   63,  125,   250, 500,
                                  1000, 2000, 4000, 8000, 16000])
    bands.third_real = np.array([12.5,     16,    20,     25,  31.5,     40,
                                 50,       63,    80,    100,   125,    160,
                                 200,     250,   315,    400,   500,    630,
                                 800,    1000,  1250,   1600,  2000,   2500,
                                 3150,   4000 , 5000,   6300,  8000,  10000,
                                 12500, 16000, 20000])

def test_octave():
    generated = octave(16, 16000)
    real = octave_real
    assert_array_equal(generated, real)


def test_octave_high():
    generated = octave_high(16, 16000)
    real = octave_real * np.sqrt(2)
    assert_array_almost_equal(generated, real)


def test_octave_low():
    generated = octave_low(16, 16000)
    real = real = octave_real / np.sqrt(2)
    assert_array_almost_equal(generated, real)


def test_third():
    generated = third(12.5, 20000)
    real = third_real
    assert_array_equal(generated, real)


def test_third_high():
    generated = third_high(12.5, 20000)
    real = third_real * 2**(1/6)
    assert_array_almost_equal(generated, real)


def test_third_low():
    generated = third_low(12.5, 20000)
    real = third_real / 2**(1/6)
    assert_array_almost_equal(generated, real)


def test_third2oct():
    levels = np.array([100, 95, 80, 55, 65, 85, 75, 70, 90, 95, 105, 110])
    generated = third2oct(levels)
    real = np.array([101.2261812, 85.0475116, 90.1771047, 111.2964174])
    assert_array_almost_equal(generated, real)


def test_third2oct_2darray():
    levels = np.array([[100, 95, 80, 55, 65, 85, 75, 70, 90, 95, 105, 110],
                       [100, 95, 80, 55, 65, 85, 75, 70, 90, 95, 105, 110]])
    generated = third2oct(levels)
    real = np.array([[101.2261812, 85.0475116, 90.1771047, 111.2964174],
                     [101.2261812, 85.0475116, 90.1771047, 111.2964174]])
    assert_array_almost_equal(generated, real)


@pytest.mark.parametrize("freqs, expected", [
    (np.array([125,  250,  500]), 'octave'),
    (np.array([12.5 , 16,   20]), 'third'),
    (np.array([125,  250, 1000, 4000]), 'octave-unsorted'),
    (np.array([12.5, 800,  500, 5000]), 'third-unsorted'),
    (np.array([100,  200,  300, 400]), None),
])
def test__check_band_type(freqs, expected):
    band_type = _check_band_type(freqs)
    assert_array_equal(band_type, expected)


def teardown_module(bands):
    pass
