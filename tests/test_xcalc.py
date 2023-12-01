import pytest  # noqa
from pyhomogenize import open_xrdataset

import index_calculator as xcalc

from .conftest import (
    pr_day_netcdf,
    snw_day_netcdf,
    tas_1hr_netcdf,
    tas_day_netcdf,
    tas_eobs_day_netcdf,
    uas_day_netcdf,
    vas_day_netcdf,
)


def test_processing():
    data = tas_day_netcdf()
    tas_ds = open_xrdataset(data)
    preproc = xcalc.preprocessing(
        tas_ds,
        freq="week",
        crop_time_axis=False,
        project="CORDEX",
    )
    proc = xcalc.processing("TG", preproc_obj=preproc)
    postproc = xcalc.postprocessing(
        proc_obj=proc,
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
    )
    xcalc.outputwriter(postproc_obj=postproc)


def test_time_range_index_calculator():
    data = tas_day_netcdf()
    tas_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
        time_range=["2001-01-01", "2001-01-07"],
    )


def test_thresh_index_calculator():
    data = pr_day_netcdf()
    pr_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RX3day",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        thresh=3,
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )


def test_perc_index_calculator():
    data = pr_day_netcdf()
    pr_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RR95p",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
        base_period_time_range=["2001-01-01", "2001-01-07"],
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="R95p",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
        base_period_time_range=["2001-01-01", "2001-01-07"],
    )


def test_snw_index_calculator():
    data = snw_day_netcdf()
    snw_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=snw_ds,
        freq="week",
        index="SCD",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )


def test_snw_const_index_calculator():
    data = snw_day_netcdf()
    snw_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=snw_ds,
        freq="week",
        index="SCD",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
        const="300 kg m-3",
    )


def test_uas_vas_index_calculator():
    data_uas = uas_day_netcdf()
    data_vas = vas_day_netcdf()
    sfcWind_ds = open_xrdataset([data_uas, data_vas])
    xcalc.index_calculator(
        ds=sfcWind_ds,
        freq="week",
        index="FG",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )


def test_1hr_index_calculator():
    data = tas_1hr_netcdf()
    tas_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )


def test_eobs_index_calculator():
    data = tas_eobs_day_netcdf()
    tas_ds = open_xrdataset(data)
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        crop_time_axis=False,
        project="EOBS",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )
