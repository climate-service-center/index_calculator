import numpy as np
import pytest  # noqa

import index_calculator._indices as indices

from .conftest import (
    hurs_series,
    mrt_series,
    pr_series,
    prsn_series,
    rlds_series,
    rlus_series,
    rsds_series,
    rsus_series,
    sfcWind_series,
    snd_series,
    tas_series,
    tasmax_series,
    tasmin_series,
)


def tas_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tas_series(np.array(series) + 273.15)


def tas_c_xarray(series=[-15, -11, 0, 26, -32, 17, -9]):
    return tas_series(np.array(series) + 273.15)


def tasmin_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tasmin_series(np.array(series) + 273.15)


def tasmax_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return tasmax_series(np.array(series) + 273.15)


def pr_xarray(series=[3, 4, 20, 20, 0, 6, 9]):
    return pr_series(np.array(series) / 86400)


def prsn_xarray(series=[7, 0, 0.5, 10, 6, 0, 4]):
    return prsn_series(np.array(series) / 86400)


def snd_xarray(series=[0, 20, 150, 340, 170, 90, 0]):
    return snd_series(np.array(series) / 100)


def hurs_xarray(series=[50, 75, 25, 90, 10, 60, 30]):
    return hurs_series(np.array(series))


def rsds_xarray(series=[200, 250, 300, 350, 270, 230, 180]):
    return rsds_series(np.array(series))


def rsus_xarray(series=[30, 50, 100, 150, 70, 30, 8]):
    return rsus_series(np.array(series))


def rlds_xarray(series=[200, 250, 300, 350, 270, 230, 180]):
    return rlds_series(np.array(series))


def rlus_xarray(series=[30, 50, 100, 150, 70, 30, 8]):
    return rlus_series(np.array(series))


def sfcWind_xarray(series=[2, 18, 5, 10, 23, 1, 7]):
    return sfcWind_series(np.array(series))


def mrt_xarray(series=[-1, -10, 0, 15, 32, 6, -8]):
    return mrt_series(np.array(series))


def test_TG():
    result = indices.TG.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TG10p():
    result = indices.TG10p.compute(
        tas=tas_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TG90p():
    result = indices.TG90p.compute(
        tas=tas_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RR():
    result = indices.RR.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_SDII():
    result = indices.SDII.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 10.33, rtol=1e-03)


def test_RR1():
    result = indices.RR1.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 6, rtol=1e-03)


def test_R10mm():
    result = indices.R10mm.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R20mm():
    result = indices.R20mm.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R25mm():
    result = indices.R25mm.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RYYmm():
    result = indices.RYYmm.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_R30mm():
    result = indices.RYYmm.compute(pr=pr_xarray(), freq="7D", thresh=30)
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_DD():
    result = indices.DD.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CDD():
    result = indices.CDD.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CWD():
    result = indices.CWD.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 4, rtol=1e-03)


def test_RX1day():
    result = indices.RX1day.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 20, rtol=1e-03)


def test_RXYYday():
    result = indices.RXYYday.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 55, rtol=1e-03)


def test_RX7day():
    result = indices.RXYYday.compute(pr=pr_xarray(), freq="7D", thresh=7)
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_TR():
    result = indices.TR.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_SQI():
    result = indices.SQI.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_FD():
    result = indices.FD.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_ID():
    result = indices.ID.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_TX():
    result = indices.TX.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TX10p():
    result = indices.TX10p.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TX90p():
    result = indices.TX90p.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TXn():
    result = indices.TXn.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 263.15, rtol=1e-03)


def test_TXx():
    result = indices.TXx.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 305.15, rtol=1e-03)


def test_TN():
    result = indices.TN.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TN10p():
    result = indices.TN10p.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TN90p():
    result = indices.TN90p.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TNn():
    result = indices.TNn.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 263.15, rtol=1e-03)


def test_TNx():
    result = indices.TNx.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 305.15, rtol=1e-03)


def test_SU():
    result = indices.SU.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CSU():
    result = indices.CSU.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_DSP():
    result = indices.DSP.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RDYYp():
    result = indices.RDYYp.compute(
        pr=pr_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_RD90p():
    result = indices.RDYYp.compute(
        pr=pr_xarray(),
        perc=90,
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RYYpTOT():
    result = indices.RYYpTOT.compute(
        pr=pr_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0.1452, rtol=1e-03)


def test_R90pTOT():
    result = indices.RYYpTOT.compute(
        pr=pr_xarray(),
        perc=90,
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CFD():
    result = indices.CFD.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_GD():
    result = indices.GD.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 41, rtol=1e-03)


def test_GD5():
    result = indices.GD.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 41, rtol=1e-03)


def test_GDYYx():
    result = indices.GDYYx.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, np.nan, rtol=1e-03)


def test_GD5x():
    result = indices.GDYYx.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, np.nan, rtol=1e-03)


def test_HD17():
    result = indices.HD17.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 100, rtol=1e-03)


def test_PRCPTOT():
    result = indices.PRCPTOT.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_CSDI():
    result = indices.CSDI.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WSDI():
    result = indices.WSDI.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CHDYYx():
    result = indices.CHDYYx.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CHD30x():
    result = indices.CHDYYx.compute(
        thresh=30,
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CW():
    result = indices.CW.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CD():
    result = indices.CD.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WW():
    result = indices.WW.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WD():
    result = indices.WD.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_DTR():
    result = indices.DTR.compute(
        tasmin=tasmin_xarray(),
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CSf():
    result = indices.CSf.compute(
        tas=tas_c_xarray(),
        freq="7D",
        thresh=-10,
        window=1,
    )
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_HSf():
    result = indices.HSf.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        thresh=27,
        window=1,
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_HSx():
    result = indices.HSx.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        thresh=27,
        window=1,
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_SD():
    result = indices.SD.compute(
        prsn=prsn_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 5, rtol=1e-03)


def test_SCD():
    result = indices.SCD.compute(
        snd=snd_xarray(),
        thresh=2,
        freq="7D",
    )
    np.testing.assert_allclose(result, 5, rtol=1e-03)


def test_Sfreq():
    result = indices.Sfreq.compute(prsn=prsn_xarray(), freq="7D")
    np.testing.assert_allclose(result, 5 / 7 * 100, rtol=1e-03)


def test_Sint():
    result = indices.Sint.compute(
        prsn=prsn_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 17.63, rtol=1e-03)


def test_UTCI():
    result = indices.UTCI.compute(
        tas=tas_xarray(),
        hurs=hurs_xarray(),
        sfcWind=sfcWind_xarray(),
        mrt=mrt_xarray(),
    )
    np.testing.assert_allclose(result, [np.nan] * 7, rtol=1e-03)
