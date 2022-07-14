import numpy as np
import pytest  # noqa

from index_calculator._indices import ClimateIndices

from .conftest import pr_series, tas_series, tasmax_series, tasmin_series


def tas_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tas_series(np.array(series) + 273.15)


def tasmin_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tasmin_series(np.array(series) + 273.15)


def tasmax_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tasmax_series(np.array(series) + 273.15)


def pr_xarray(series=[3, 4, 20, 20, 0, 6, 9]):
    return pr_series(np.array(series) / 86400)


def test_TG():
    result = ClimateIndices().TG(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_RR():
    result = ClimateIndices().RR(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_SDII():
    result = ClimateIndices().SDII(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 10.33, rtol=1e-03)


def test_RR1():
    result = ClimateIndices().RR1(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 6, rtol=1e-03)


def test_R10mm():
    result = ClimateIndices().R10mm(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R20mm():
    result = ClimateIndices().R20mm(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R25mm():
    result = ClimateIndices().R25mm(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_DD():
    result = ClimateIndices().DD(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CDD():
    result = ClimateIndices().CDD(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CWD():
    result = ClimateIndices().CWD(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 4, rtol=1e-03)


def test_RX1day():
    result = ClimateIndices().RX1day(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 20, rtol=1e-03)


def test_RX5day():
    result = ClimateIndices().RX5day(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 55, rtol=1e-03)


def test_TR():
    result = ClimateIndices().TR(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_SQI():
    result = ClimateIndices().SQI(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_FD():
    result = ClimateIndices().FD(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_ID():
    result = ClimateIndices().ID(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_TX():
    result = ClimateIndices().TX(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TXn():
    result = ClimateIndices().TXn(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 263.15, rtol=1e-03)


def test_TXx():
    result = ClimateIndices().TXx(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 305.15, rtol=1e-03)


def test_TN():
    result = ClimateIndices().TN(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TNn():
    result = ClimateIndices().TNn(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 263.15, rtol=1e-03)


def test_TNx():
    result = ClimateIndices().TNx(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 305.15, rtol=1e-03)


def test_SU():
    result = ClimateIndices().SU(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CSU():
    result = ClimateIndices().CSU(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)
