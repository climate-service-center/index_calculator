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
    sfcWindmax_series,
    snd_series,
    snw_series,
    tas_series,
    tasmax_series,
    tasmin_series,
)


def tas_xarray(series=[-1, -10, 0, 15, 32, 6, -8], **kwargs):
    return tas_series(np.array(series) + 273.15, **kwargs)


def tas_c_xarray(series=[-15, -11, 0, 26, -32, 17, -9], **kwargs):
    return tas_series(np.array(series) + 273.15, **kwargs)


def tasmin_xarray(series=[-11, -26, -4, 1, 24, -3, -12], **kwargs):
    return tasmin_series(np.array(series) + 273.15, **kwargs)


def tasmax_xarray(series=[-1, -10, 0, 15, 32, 6, -8], **kwargs):
    return tasmax_series(np.array(series) + 273.15, **kwargs)


def pr_xarray(series=[3, 4, 20, 20, 0, 6, 9], **kwargs):
    return pr_series(np.array(series) / 86400, **kwargs)


def prsn_xarray(series=[7, 0, 0.5, 10, 6, 0, 4], **kwargs):
    return prsn_series(np.array(series) / 86400, **kwargs)


def snd_xarray(series=[0, 20, 150, 340, 170, 90, 0], **kwargs):
    return snd_series(np.array(series) / 100, **kwargs)


def snw_xarray(series=[0, 6, 50, 110, 60, 30, 0], **kwargs):
    return snw_series(np.array(series) / 100, **kwargs)


def hurs_xarray(series=[50, 75, 25, 90, 10, 60, 30], **kwargs):
    return hurs_series(np.array(series), **kwargs)


def rsds_xarray(series=[200, 250, 300, 350, 270, 230, 180], **kwargs):
    return rsds_series(np.array(series), **kwargs)


def rsus_xarray(series=[30, 50, 100, 150, 70, 30, 8], **kwargs):
    return rsus_series(np.array(series), **kwargs)


def rlds_xarray(series=[200, 250, 300, 350, 270, 230, 180], **kwargs):
    return rlds_series(np.array(series), **kwargs)


def rlus_xarray(series=[30, 50, 100, 150, 70, 30, 8], **kwargs):
    return rlus_series(np.array(series), **kwargs)


def sfcWind_xarray(series=[2, 18, 5, 10, 23, 1, 7], **kwargs):
    return sfcWind_series(np.array(series), **kwargs)


def sfcWindmax_xarray(series=[2, 18, 5, 10, 23, 1, 7], **kwargs):
    return sfcWindmax_series(np.array(series), **kwargs)


def mrt_xarray(series=[-1, -10, 0, 15, 32, 6, -8], **kwargs):
    return mrt_series(np.array(series), **kwargs)


def test_TG():
    idx_class = indices.TG()
    result = idx_class.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TG10p():
    idx_class = indices.TG10p()
    result = idx_class.compute(
        tas=tas_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TG90p():
    idx_class = indices.TG90p()
    result = idx_class.compute(
        tas=tas_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RR():
    idx_class = indices.RR()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_SDII():
    idx_class = indices.SDII()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 10.33, rtol=1e-03)


def test_RR1():
    idx_class = indices.RR1()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 6, rtol=1e-03)


def test_R10mm():
    idx_class = indices.R10mm()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R20mm():
    idx_class = indices.R20mm()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_R25mm():
    idx_class = indices.R25mm()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RYYmm():
    idx_class = indices.RYYmm()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_R30mm():
    idx_class = indices.RYYmm()
    result = idx_class.compute(pr=pr_xarray(), freq="7D", thresh=30)
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_DD():
    idx_class = indices.DD()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CDD():
    idx_class = indices.CDD()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CWD():
    idx_class = indices.CWD()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 4, rtol=1e-03)


def test_RX1day():
    idx_class = indices.RX1day()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 20, rtol=1e-03)


def test_RXYYday():
    idx_class = indices.RXYYday()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 55, rtol=1e-03)


def test_RX7day():
    idx_class = indices.RXYYday()
    result = idx_class.compute(pr=pr_xarray(), freq="7D", window=7)
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_TR():
    idx_class = indices.TR()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_SQI():
    idx_class = indices.SQI()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_FD():
    idx_class = indices.FD()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 5, rtol=1e-03)


def test_LFD():
    idx_class = indices.LFD()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        start_date="01-04",
        end_date="01-07",
    )
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_ID():
    idx_class = indices.ID()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_TX():
    idx_class = indices.TX()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 278, rtol=1e-03)


def test_TX10p():
    idx_class = indices.TX10p()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TX90p():
    idx_class = indices.TX90p()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TXn():
    idx_class = indices.TXn()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 263.15, rtol=1e-03)


def test_TXx():
    idx_class = indices.TXx()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 305.15, rtol=1e-03)


def test_TN():
    idx_class = indices.TN()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 268.72, rtol=1e-03)


def test_TN10p():
    idx_class = indices.TN10p()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TN90p():
    idx_class = indices.TN90p()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_TNn():
    idx_class = indices.TNn()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 247.15, rtol=1e-03)


def test_TNx():
    idx_class = indices.TNx()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 297.15, rtol=1e-03)


def test_SU():
    idx_class = indices.SU()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CSU():
    idx_class = indices.CSU()
    result = idx_class.compute(tasmax=tasmax_xarray(), freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_DSf():
    idx_class = indices.DSf()
    result = idx_class.compute(pr=pr_xarray(), window=2, freq="7D")
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_DSx():
    idx_class = indices.DSx()
    result = idx_class.compute(pr=pr_xarray(), window=1, freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_DSn():
    idx_class = indices.DSn()
    result = idx_class.compute(pr=pr_xarray(), window=1, freq="7D")
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_WSf():
    idx_class = indices.WSf()
    result = idx_class.compute(pr=pr_xarray(), window=1, freq="7D")
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_WSx():
    idx_class = indices.WSx()
    result = idx_class.compute(pr=pr_xarray(), window=1, freq="7D")
    np.testing.assert_allclose(result, 4.0, rtol=1e-03)


def test_WSn():
    idx_class = indices.WSn()
    result = idx_class.compute(pr=pr_xarray(), window=1, freq="7D")
    np.testing.assert_allclose(result, 6.0, rtol=1e-03)


def test_RYYp():
    idx_class = indices.RYYp()
    result = idx_class.compute(
        pr=pr_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RRYYp():
    idx_class = indices.RRYYp()
    result = idx_class.compute(
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    expected = [
        2.0062e-04,
        2.3148e-04,
        2.3148e-04,
        2.3148e-04,
        2.3148e-04,
        2.1026e-04,
        1.0417e-04,
    ]
    np.testing.assert_allclose(result, expected, rtol=1e-03)


def test_RYYp_perc():
    pr = pr_xarray()
    idx_class = indices.RRYYp()
    per = idx_class.compute(
        pr=pr,
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    idx_class = indices.RYYp()
    result = idx_class.compute(
        pr=pr,
        per=per,
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_R90p():
    idx_class = indices.RYYp()
    result = idx_class.compute(
        pr=pr_xarray(),
        per=90,
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_RYYpTOT():
    idx_class = indices.RYYpTOT()
    result = idx_class.compute(
        pr=pr_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_R90pTOT():
    idx_class = indices.RYYpTOT()
    result = idx_class.compute(
        pr=pr_xarray(),
        per=90,
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CFD():
    idx_class = indices.CFD()
    result = idx_class.compute(tasmin=tasmin_xarray(), freq="7D")
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_GD():
    idx_class = indices.GD()
    result = idx_class.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 41, rtol=1e-03)


def test_GD5():
    idx_class = indices.GD()
    result = idx_class.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 41, rtol=1e-03)


def test_HD17():
    idx_class = indices.HD17()
    result = idx_class.compute(tas=tas_xarray(), freq="7D")
    np.testing.assert_allclose(result, 100, rtol=1e-03)


def test_PRCPTOT():
    idx_class = indices.PRCPTOT()
    result = idx_class.compute(pr=pr_xarray(), freq="7D")
    np.testing.assert_allclose(result, 62, rtol=1e-03)


def test_CSDI():
    idx_class = indices.CSDI()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WSDI():
    idx_class = indices.WSDI()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        base_period_time_range=["2000-01-01", "2000-01-07"],
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CHDYYx():
    idx_class = indices.CHDYYx()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CHD30x():
    idx_class = indices.CHDYYx()
    result = idx_class.compute(
        thresh=30,
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_CW():
    idx_class = indices.CW()
    result = idx_class.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_CD():
    idx_class = indices.CD()
    result = idx_class.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WW():
    idx_class = indices.WW()
    result = idx_class.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_WD():
    idx_class = indices.WD()
    result = idx_class.compute(
        tas=tas_xarray(),
        pr=pr_xarray(),
        base_period_time_range=["2000-01-01", "2000-01-07"],
        freq="7D",
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_DTR():
    idx_class = indices.DTR()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        tasmax=tasmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 9.29, rtol=1e-03)


def test_CSf():
    idx_class = indices.CSf()
    result = idx_class.compute(
        tas=tas_c_xarray(),
        freq="7D",
        thresh=-10,
        window=1,
    )
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_CSx():
    idx_class = indices.CSx()
    result = idx_class.compute(
        tas=tas_c_xarray(),
        freq="7D",
        thresh=-10,
    )
    np.testing.assert_allclose(result, 2, rtol=1e-03)


def test_CSn():
    idx_class = indices.CSn()
    result = idx_class.compute(
        tas=tas_c_xarray(),
        freq="7D",
        thresh=-10,
        window=1,
    )
    np.testing.assert_allclose(result, 3, rtol=1e-03)


def test_HSf():
    idx_class = indices.HSf()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        thresh=27,
        window=1,
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_HSx():
    idx_class = indices.HSx()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        thresh=27,
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_HSn():
    idx_class = indices.HSn()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        freq="7D",
        thresh=27,
        window=1,
    )
    np.testing.assert_allclose(result, 1, rtol=1e-03)


def test_HWx():
    idx_class = indices.HWx()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        tasmin=tasmin_xarray(),
        freq="7D",
        thresh_tasmax=27,
        thresh_tasmin=25,
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_HWf():
    idx_class = indices.HWf()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        tasmin=tasmin_xarray(),
        freq="7D",
        thresh_tasmax=27,
        thresh_tasmin=25,
        window=1,
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_HWn():
    idx_class = indices.HWn()
    result = idx_class.compute(
        tasmax=tasmax_xarray(),
        tasmin=tasmin_xarray(),
        freq="7D",
        thresh_tasmax=27,
        thresh_tasmin=25,
        window=1,
    )
    np.testing.assert_allclose(result, 0, rtol=1e-03)


def test_SD():
    idx_class = indices.SD()
    result = idx_class.compute(
        prsn=prsn_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 4, rtol=1e-03)


def test_SCD():
    idx_class = indices.SCD()
    result = idx_class.compute(
        snd=snd_xarray(),
        thresh=2,
        freq="7D",
        window=1,
    )
    np.testing.assert_allclose(result, 5, rtol=1e-03)


def test_Sfreq():
    idx_class = indices.Sfreq()
    result = idx_class.compute(prsn=prsn_xarray(), freq="7D")
    np.testing.assert_allclose(result, 4 / 7 * 100, rtol=1e-03)


def test_Sint():
    idx_class = indices.Sint()
    result = idx_class.compute(
        prsn=prsn_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, 6.75, rtol=1e-03)


def test_UTCI():
    idx_class = indices.UTCI()
    result = idx_class.compute(
        tas=tas_xarray(),
        hurs=hurs_xarray(),
        sfcWind=sfcWind_xarray(),
        mrt=mrt_xarray(),
    )
    np.testing.assert_allclose(result, [np.nan] * 7, rtol=1e-03)


def test_WI():
    idx_class = indices.WI()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [3], rtol=1e-03)


def test_GSS():
    idx_class = indices.GSS()
    result = idx_class.compute(
        tas=tas_xarray(),
        window=1,
        freq="7D",
    )
    np.testing.assert_allclose(result, [np.nan], rtol=1e-03)


def test_GSE():
    idx_class = indices.GSE()
    result = idx_class.compute(
        tas=tas_xarray(),
        window=1,
        freq="7D",
    )
    np.testing.assert_allclose(result, [np.nan], rtol=1e-03)


def test_GSL():
    idx_class = indices.GSL()
    result = idx_class.compute(
        tas=tas_xarray(),
        window=1,
        freq="7D",
    )
    np.testing.assert_allclose(result, [0.0], rtol=1e-03)


def test_FFS():
    idx_class = indices.FFS()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        window=1,
        freq="7D",
    )
    np.testing.assert_allclose(result, [np.nan], rtol=1e-03)


def test_FFE():
    idx_class = indices.FFE()
    result = idx_class.compute(
        tasmin=tasmin_xarray(),
        window=1,
        freq="7D",
    )
    np.testing.assert_allclose(result, [np.nan], rtol=1e-03)


def test_RRm():
    idx_class = indices.RRm()
    result = idx_class.compute(
        pr=pr_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [8.857], rtol=1e-03)


def test_FG():
    idx_class = indices.FG()
    result = idx_class.compute(
        sfcWind=sfcWind_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [9.429], rtol=1e-03)


def test_FGn():
    idx_class = indices.FGn()
    result = idx_class.compute(
        sfcWind=sfcWind_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [1], rtol=1e-03)


def test_FGx():
    idx_class = indices.FGx()
    result = idx_class.compute(
        sfcWind=sfcWind_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [23], rtol=1e-03)


def test_FX():
    idx_class = indices.FX()
    result = idx_class.compute(
        sfcWindmax=sfcWindmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [9.429], rtol=1e-03)


def test_FXn():
    idx_class = indices.FXn()
    result = idx_class.compute(
        sfcWindmax=sfcWindmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [1], rtol=1e-03)


def test_FXx():
    idx_class = indices.FXx()
    result = idx_class.compute(
        sfcWindmax=sfcWindmax_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [23], rtol=1e-03)


def test_HIX():
    idx_class = indices.HIX()
    result = idx_class.compute(
        tas=tas_xarray(),
        hurs=hurs_xarray(),
    )
    np.testing.assert_allclose(
        result,
        [-4.977235, -14.36269, -4.706667, 17.962594, 29.079492, 3.561291, -12.997314],
        rtol=1e-03,
    )


def test_CMD():
    idx_class = indices.CMD()
    result = idx_class.compute(
        sfcWind=sfcWind_xarray(),
        freq="7D",
    )
    np.testing.assert_allclose(result, [1], rtol=1e-03)
