import numpy as np

from jwst_galaxy_analysis.photometry import abmag_error_from_flux, percentile_errors


def test_percentile_errors():
    median = np.array([10.0, 11.0])
    low = np.array([9.7, 10.4])
    high = np.array([10.4, 11.9])
    lo, hi = percentile_errors(median, low, high)
    np.testing.assert_allclose(lo, [0.3, 0.6])
    np.testing.assert_allclose(hi, [0.4, 0.9])


def test_abmag_error_from_flux():
    err = abmag_error_from_flux(np.array([100.0]), np.array([10.0]))
    np.testing.assert_allclose(err, [(2.5 / np.log(10.0)) * 0.1])


def test_abmag_error_invalid_flux_is_nan():
    err = abmag_error_from_flux(np.array([-1.0, 0.0]), np.array([1.0, 1.0]))
    assert np.isnan(err).all()
